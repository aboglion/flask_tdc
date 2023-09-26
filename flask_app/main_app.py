from flask import Flask, render_template,request, redirect, url_for, session,make_response
from dotenv import dotenv_values 
import os
import TDC_parse_eb.TDC_parse_eb as TDC
import TDC_parse_eb.TDC_parse_eb_utils.Consts as Consts
from tinydb import TinyDB, Query
import hashlib,time
from datetime import datetime,timedelta

if not os.path.exists(Consts.DB_JASON):
    os.makedirs(Consts.DB_JASON)

#תאריך עדכון הבסיס נתונים יום לפני בהפעלה ראשונה
try:
    with open(f'./TDC_parse_eb/UPDATE_DATE.log', "r") as UPDATE_DATE_FILE:
        updated_date=int(UPDATE_DATE_FILE.read())
except Exception as e:
        print(e)
        with open(f'./TDC_parse_eb/UPDATE_DATE.log', "w+") as UPDATE_DATE_FILE:
            updated_date = (datetime.now() - timedelta(days=1)).day
            UPDATE_DATE_FILE.write(str(updated_date))
            


app = Flask(__name__)
ALL_Plant = Consts.NET_B+Consts.NET_A


@app.route('/')
def main_page():
    global updated_date
    # השגת המידע לדף הראשי
    PMs_DB = TinyDB(f'{Consts.DB_JASON}/PMs.json')
    data_main = PMs_DB.all()
    PMs_DB.close()
    # אם לא קיים מידע בבסיס נתונים אז תעשה עדכון לשליפה מהקבצים
    # or
    # אם התאריך לא מעודכן והשעה אחרי תשע בבוקר אז לעדכן בסיס הנתונים ולעדכן תאריך עדכון
                # (פתיחת האתר הראשונה אחרי השעה 9 יתעדכן הבסיס נתונים)    
    if not data_main or ( updated_date!=datetime.now().day and  datetime.now().hour >= Consts.update_hour):
        with open(f'./TDC_parse_eb/UPDATE_DATE.log', "w+") as UPDATE_DATE_FILE:
            updated_date = datetime.now().day
            UPDATE_DATE_FILE.write(str(updated_date))
        return render_template('update_page.html')
    return render_template('main.html', data=data_main[0])

#דף להצגת הודעה ואנימאשין להמתנה 
@app.route('/update_page/')
def update_page():
    return render_template('update_page.html')
@app.route('/update/') # הפעלת הפונקציה של העדכון
def update_LYOUT():
        # פתיחת הקובץ של תגים וכפליות לכתיבה (אם הוא קיים הקובץ יימחק ואם לא, הוא ייווצר)
    with open('templates/duplication.html', 'w', encoding="utf-8") as file:
        file.write("<html>\n<head>\n<title> תגים - כפליות </title>\n</head>\n<body>\n")
        file.write("</body>\n</html>")
    for which_plant in ALL_Plant:
        TDC.main_parser(which_plant)
    with open('templates/duplication.html', 'a', encoding="utf-8") as file:
        file.write("</body>\n</html>")
    r=False
    while (not r):
        time.sleep(2)
        r=TDC.Parse_Utils.Update_Pms_Data()

    print("updated")
    return redirect(url_for('main_page'))

@app.route('/duplication/', methods=['POST', 'GET'])
def duplication():
    return render_template('duplication.html')




# The string to be hashed TODO:setup dotenv for token
#app.secret_key =  SECRIT["HASH_KEY"]
app.secret_key =  os.getenv("HASH_KEY")

def hash_password(password):
    hash_object = hashlib.sha256()
    hash_object.update(password.encode('utf-8'))
    return hash_object.hexdigest()

@app.route('/login/', methods=['POST', 'GET'])
def log_in():
    error = None
    if request.method == 'POST':
        password = request.form['password']
        if (hash_password(password) == app.secret_key):
            session['logged_in'] = True
            return redirect(url_for('main_page'))
        else:
            error = 'Invalid password. Please try again.'
    return render_template('login.html', error=error)


@app.route('/logout/', methods=['POST', 'GET'])
def log_out():
    session['logged_in'] = False
    return redirect(url_for('main_page'))



# http://localhost:5000/tags_table/~/~/~/~/~/~/~/~/~/~/~/~/~/~/~/~/0/0
@app.route('/tags_table/<NAME>/<PTDESC>/<SLOTNUM>/<ID>/<STATUS>/<TYPE>/<NODENUM>/<PLANT>/<DB_FILE>/<DISRC_1>/<DISRC_2>/<DODSTN_1>/<DODSTN_2>/<CODSTN_1>/<CISRC_1>/<CISRC_2>/<num>/<foucs_id>')
@app.route('/tags_table/')
def tags_table(num=0, filter=None, NAME=" ", PTDESC='', SLOTNUM='', ID='', STATUS='', TYPE='', NODENUM='', PLANT='', DB_FILE='', DISRC_1='', DISRC_2='', DODSTN_1='', DODSTN_2='', CODSTN_1='', CISRC_1='', CISRC_2='', foucs_id=""):
    # var_dict קבלת המשתנים מהלינק
    var_dict = {"NAME": str(NAME).upper(), "PTDESC": str(PTDESC).upper(), "SLOTNUM": SLOTNUM, "ID": ID, "STATUS": STATUS, "TYPE":str(TYPE).upper() , "NODENUM": NODENUM, "PLANT": PLANT, "DB_FILE":str(DB_FILE).upper() ,
                "DISRC_1": str(DISRC_1).upper(), "DISRC_2": str(DISRC_2).upper(), "DODSTN_1": str(DODSTN_1).upper() , "DODSTN_2": str(DODSTN_2).upper() , "CODSTN_1": str(CODSTN_1).upper() , "CISRC_1":str(CISRC_1).upper() , "CISRC_2":str(CISRC_2).upper() }
    points = []  
    variables = []  #כל המשתנים 
    quary_dict_clean = {} # יכיל את כל המתשנים שלא ריקים 
    # ייצירת מילון לחפוש מהלינק
    for K in var_dict:
        variables.append(var_dict[K])
        if not (var_dict[K] == '~' or var_dict[K].strip() == ''):
            quary_dict_clean[f'{K}'] = var_dict[K] 
    TAGS = Query()

    # בדיקת אם המתקן נמצא במילון החיפוש
    # יבוא מידע רק של המתקן הספיציי
    if "PLANT" in quary_dict_clean: #אם הוגדר מתקן ספציפי
        which_plant = quary_dict_clean['PLANT']
        if not which_plant in ALL_Plant: #לבדוק אם לא הכניסו סתם שם של מתקן הכתובת
            points = []
            serch_plant = []
        else:
            serch_plant = [which_plant]
    else:
        serch_plant = ALL_Plant #אם לא הוגדר מתקן ספציפי
    # quary_dict_clean get from url and clean empty ,to filterat keys data
    points = GET_TAGS(serch_plant, quary_dict_clean)
    try:  #num זה מספר העמוד
        num = int(num) # אם לא הוכנס מספר עמוד או שהוא לא תקין אז תקח עמוד 0
    except Exception:
        num = 0
    if num <= 0: #כדי לעשות את הגלילה מעגלית של העמודים  אם שלילי אז תבוא להתחלה עמוד 0
        #foucs_id =איזה תא חיפוש הפוקס היה נמצא כדי להחזיר אותו לשם
        return render_template('table_tags.html', data=points[:100], l=0, variables=variables, foucs_id=foucs_id)
    if len(points) > (num)*100: # כל פעם קח 100 
        return render_template('table_tags.html', data=points[(num-1)*100:(num)*100], l=num, variables=variables, foucs_id=foucs_id)
    return render_template('table_tags.html', data=points[(num-1)*100:], l=0, variables=variables, foucs_id=foucs_id)


# http://localhost:5000/LYOUT/800/7/
@app.route('/LYOUT/<int:plant>/<int:pm>/')
def LYOUT(plant=800, pm=5):
    plant = str(plant)
    pm = str(pm) if len(str(pm)) > 1 else "0"+str(pm)
    LYOUT_DB = TinyDB(f'{Consts.DB_JASON}/LYOUT_DB_{plant}.json')
    LYOUT_DATA = LYOUT_DB.all()[0][plant][pm]
    LYOUT_DB.close()
    return render_template('LYOUT.html', lyout=LYOUT_DATA, plant=str(plant), pm=str(pm))


# post שינוי תג ידני מהדף של הטבלה LYOUT
@app.route('/updateit', methods=['POST'])
def updateit() :
        it = request.get_json() 
        lyputpm='0'+it["PM"] if len(it["PM"])<2 else it["PM"]
        # print(it,"<----------------------------==========")
        LYOUT_DB = TinyDB(f'{Consts.DB_JASON}/LYOUT_DB_{it["PLANT"]}.json')
        LYOUT_DATA = LYOUT_DB.all()[0]#[it["PLANT"]][it["PM"]][it["CARD_NUM"]])
        LYOUT_DATA[it["PLANT"]][lyputpm][str(it["CARD_NUM"])][int(it["POINT_NUM"])-1]=it
        LYOUT_DB.truncate()
        LYOUT_DB.insert(LYOUT_DATA)
        LYOUT_DB.close
        TA_DB = TinyDB(f'{Consts.DB_JASON}/TAGS_DB_{it["PLANT"]}.json')
        tags=TA_DB.all()[0][it["PLANT"]]
        s_t=[t for t in tags if t["ID"]!=it["ID"]]
        s_t.append(it)
        TA_DB.truncate()
        TA_DB.insert({it["PLANT"]:s_t}) 
        TA_DB.close() 
        response = make_response('Success', 200)
        return response

# פונקציות עזר
# ===========

def GET_TAGS(plants, quary_dict_clean):
    re = []
    name = False   # אם יש חיפוש על השם
    desc = False   #אם יש חיפוש על דיסקרפשן
    if "NAME" in quary_dict_clean: # השם והדיסקרפשין לא רוצים לפלטר במדויק לכן נשמרים על נמנת לעשות חיפוש על חלק מהמילה ולא המילה המדוייקת
        name = quary_dict_clean["NAME"]
        del quary_dict_clean["NAME"]
    if "PTDESC" in quary_dict_clean:
        desc = quary_dict_clean["PTDESC"]
        del quary_dict_clean["PTDESC"]
    for which_plant in plants:
        TAGS_DB = TinyDB(f'{Consts.DB_JASON}/TAGS_DB_{which_plant}.json')
        DATA = list(TAGS_DB.all())
        if len(DATA) > 0:
            TAGS_DATA = DATA[0][which_plant]
            # במדויק -אם הערכים לחיפוש נמצאים אז לפלטר רק את הנתונים שיש להן אותם
            if (quary_dict_clean):
                TAGS_DATA = filter_dicts(list(TAGS_DATA), quary_dict_clean)
            re.extend(TAGS_DATA)
        else:
            continue
        TAGS_DB.close()
    # re = חיפוש חלק מהמילה - ריגולר אקספרשן
    if name:
     #הכנס אליו את האיברים שיש להם דיסקרפשין שחלק ממנו נמצא אם לא נמצא החזר ריק
        re = [d for d in re if name in d.get("NAME", "")]
        # re = [d for d in re if d.get(
        #     "NAME", "").startswith(str(name).upper())]
    if desc:
        #הכנס אליו את האיברים שיש להם דיסקרפשין שחלק ממנו נמצא אם לא נמצא החזר ריק
        re = [d for d in re if desc in d.get("PTDESC", "")]
    return re

def filter_dicts(list_of_dicts, criteria):
    result = []
    for item in list_of_dicts:
        if all(item.get(key) == value for key, value in criteria.items()):
            result.append(item)
    return result

if __name__ == '__main__':
    app.run(debug=True)


