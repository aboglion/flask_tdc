from flask import Flask, render_template, request, redirect, url_for, session, make_response
import os,hashlib
from glob import glob
from TDC_parse_eb.pvsrc_parser import pvsrc_parse
import TDC_parse_eb.TDC_parse_eb_utils.Consts as Consts
from pvsrc import router_pvsrc
from router_sql import router_SQL,xxToSql
import Plugins
if not os.path.exists(Consts.DB_JASON):
    os.makedirs(Consts.DB_JASON)
if not os.path.exists(Consts.DB_SQL):
    os.makedirs(Consts.DB_SQL)

ALL_Plant = Consts.NET_B+Consts.NET_A

app = Flask(__name__)

app.secret_key = os.getenv("HASH_KEY")
referrer = None




@app.route('/')
def main_page():

    #CHECK Update_Data
    MainPage_Data=Plugins.Get_DBJson_Data("PMs.json")
    updated_date=Plugins.Get_Last_UpdateDate()
    actionUpdateData=Plugins.Update_Data()
    if actionUpdateData:
        return redirect(actionUpdateData)

    # global MainPage_Data,updated_date
    if not os.path.exists(Consts.DB_JASON):
        try:os.makedirs(Consts.DB_JASON)
        except Exception:return(f'\n\n THERE IS NO FOLDER {Consts.DB_JASON}\n CAN NOT MAKE NEW FOLDER')

    EB_FILES_DIR_exist=False if not os.path.exists(Consts.EB_FILES_DIR) else True
    #get the logs of copy files
    DbLogs_Dates=Plugins.Get_DbLogs_Dates()
    MainPage_Data=Plugins.Get_DBJson_Data("PMs.json")
    print(MainPage_Data)
    if len(MainPage_Data)<1:
        DbLogs_Dates={"A":["תקלה בכונן משותף גי',לבדוק עם יובל- יונס - לאוניד",],"B":["תקלה בכונן משותף גי',לבדוק עם יובל- יונס - לאוניד",]}
        MainPage_Data=[[],]
    return render_template('main.html', data=MainPage_Data[0], dates_A=DbLogs_Dates["A"], dates_B=DbLogs_Dates["B"],EB_FILES_DIR_exist=EB_FILES_DIR_exist,updated_date=updated_date)


#-====== updateing data base parsing .. =====
# דף להצגת הודעה ואנימאשין להמתנה
@app.route('/wait_update_finsh/')
def wait_update_finsh():
    return render_template('wait_update_finsh.html')

@app.route('/update/')  # הפעלת הפונקציה של העדכון
def update_LYOUT():
    Plugins.DBJson.Replace_DBJson_Data("updating_runing.json",{"updating_runing":True})
    print("run pvsrc")
    pvsrc_parse()
    print("\n out pvsrc_parse")
    print("run SMS_parse")
    Plugins.parse_SMS()
    stat_update=Plugins.RUN_Update(ALL_Plant)
    try:xxToSql(1)
    except Exception as e:pass
    print("updated --- ",stat_update)
    Plugins.DBJson.Replace_DBJson_Data("updating_runing.json",{"updating_runing":stat_update})
    return redirect(url_for('main_page'))
#--------------------------------------------------


#-====== duplication.. =====
# duplication page
@app.route('/duplication/', methods=['POST', 'GET'])
def duplication():
    duplication_data = Plugins.Get_DBJson_Data("duplication_db.json")
    return render_template('duplication.html', data=duplication_data)
##--------------------------   

#-====== SMS USME.. =====
# main_sms page
@app.route('/SMS_UCME/', methods=['POST', 'GET'])
def SMS_UCME():
    try: 
        with open(Consts.SMS_HTML_outmain, 'r') as file:
            html = file.read()  # קורא את כל השורות לרשימה
    except Exception as e :html=f"{e}\n{Consts.SMS_HTML_outmain} NOT FOUND"
    return (html)
# groups_sms page
@app.route('/GROUPS.html/', methods=['POST', 'GET'])
def GROUPS():
    try: 
        with open(Consts.SMS_out_groups, 'r', encoding='iso-8859-8') as file:
            html = file.read()  # קורא את כל השורות לרשימה
    except Exception as e :html=f"{e}\n{Consts.SMS_out_groups} NOT FOUND"
    return (html)
##--------------------------   

####-------------PVSRC router
router_pvsrc(app)
##--------------------------   

####-------------SQL-lite router
router_SQL(app)
@app.route('/sql/', methods=['POST', 'GET'])
def sq():
    xxToSql(1)
    return "Welcome"
##--------------------------  

@app.route('/login/', methods=['POST', 'GET'])
def log_in():
    print("log_in_page >>><<<<<<")
    global referrer #הדף האחרון שהינו בו כדי לחזור אליו במידה והצלחנו לכנס
    if request.method == 'POST':  # זה פוסט בא מהפורם לאחר הכנסת הסיסמה    
        hash_object = hashlib.sha256()
        password=request.form['password']
        hash_object.update(password.encode('utf-8'))
        if hash_object.hexdigest() == app.secret_key: #בדיקת סיסמה אם נכונה
            session['logged_in'] = True
            return redirect(referrer if referrer else url_for('main_page'))
        else: return render_template('login.html', error='Invalid password. Please try again.') #סיסמה לא נכונה
    else:  # אם זה לא פוסט (כניסה ראשונה לדף) תשמור לי את הדף שבאת ממנו
            if (request.referrer and 'login' not in request.referrer):referrer = request.referrer
            return render_template('login.html', error=None)


@app.route('/logout/', methods=['POST', 'GET'])
def log_out():
    global referrer
    session['logged_in'] = False
    referrer = request.referrer if ('log' not in request.referrer) else referrer
    if referrer :return redirect(referrer)
    else:redirect(url_for('main_page'))

# http://localhost:5000/tags_table/~/~/~/~/~/~/~/~/~/~/~/~/~/~/~/~/0/0
@app.route('/tags_table/<NAME>/<PTDESC>/<SLOTNUM>/<ID>/<STATUS>/<TYPE>/<NODENUM>/<PLANT>/<DB_FILE>/<DISRC_1>/<DISRC_2>/<DODSTN_1>/<DODSTN_2>/<CODSTN_1>/<CISRC_1>/<CISRC_2>/<num>/<foucs_id>')
@app.route('/tags_table/')
def tags_table( NAME="~", PTDESC="~", SLOTNUM="~", ID="~", STATUS="~", TYPE='~', NODENUM="~", PLANT="~", DB_FILE="~", DISRC_1="~", DISRC_2="~", DODSTN_1="~", DODSTN_2="~", CODSTN_1="~", CISRC_1="~", CISRC_2="~", num='0',foucs_id=""):
    
    #CHECK Update_Data
    actionUpdateData=Plugins.Update_Data()
    if actionUpdateData:return redirect(actionUpdateData)
    
    # var_dict קבלת המשתנים מהלינק
    var_dict = dict(list(locals().items())[:-3])
    points = []
    variables_all = []  # כל המשתנים
    varibles_for_search = {}  # יכיל את כל המתשנים שלא ריקים
    # ייצירת מילון לחפוש מהלינק
    for K in var_dict:
        upper_var = var_dict[K] if type(var_dict[K])==int else var_dict[K].upper()
        variables_all.append(upper_var)

        if not (var_dict[K] == '~' or var_dict[K].strip() == ''):
            varibles_for_search[f'{K}'] = upper_var

    
    points = Plugins.Filtered_Sarch(ALL_Plant, varibles_for_search)

    try:  # num זה מספר העמוד
        num = int(num)  # אם לא הוכנס מספר עמוד או שהוא לא תקין אז תקח עמוד 0
    except Exception:
        num = 0
    if num <= 0:  # כדי לעשות את הגלילה מעגלית של העמודים  אם שלילי אז תבוא להתחלה עמוד 0
        # foucs_id =איזה תא חיפוש הפוקס היה נמצא כדי להחזיר אותו לשם
        return render_template('table_tags.html', data=points[:100], l=0, variables=variables_all, foucs_id=foucs_id)
    if len(points) > (num)*100:  # כל פעם קח 100
        return render_template('table_tags.html', data=points[(num-1)*100:(num)*100], l=num, variables=variables_all, foucs_id=foucs_id)
    return render_template('table_tags.html', data=points[(num-1)*100:], l=0, variables=variables_all, foucs_id=foucs_id)


# http://localhost:5000/LYOUT/800/7/ : דוגמה 
@app.route('/LYOUT/<int:plant>/<int:pm>/')
def LYOUT(plant=800, pm=5):

    #CHECK Update_Data
    actionUpdateData=Plugins.Update_Data()
    if actionUpdateData:return redirect(actionUpdateData)

    plant = str(plant) # לשנות לסטרינג 
    pm = str(pm) if pm > 9 else "0"+str(pm) #לעשות שיהיה שתי ספרות 
    try:LYOUT_DATA = Plugins.Get_DBJson_Data(f'LYOUT_DB_{plant}.json')[0][plant][pm]
    except:return "404 NO DATA FOR THIS PM / PLANT"
    return render_template('LYOUT.html', lyout=LYOUT_DATA, plant=plant, pm=pm)



# post שינוי תג ידני מהדף של הטבלה LYOUT
@app.route('/updateit', methods=['POST'])
def updateit():
    if session['logged_in'] == True:
       # להוציא את שם הבקר והמתקן והבסיס נתונים מתוך התג שרוצים לשנות
        it = request.get_json()
        Plugins.Update_DBJson_Data(it)
        response = make_response('Success', 200)
        return response



if __name__ == '__main__':
    Consts.runmode(app)



