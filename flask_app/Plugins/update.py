from datetime import datetime, timedelta
from tinydb import TinyDB, Query
import TDC_parse_eb.TDC_parse_eb as TDC
import os
from .DBJson import Replace_DBJson_Data,Get_DBJson_Data
import TDC_parse_eb.TDC_parse_eb_utils.Consts as Consts

# UPDATE


def Get_Last_UpdateDate():
    # תאריך עדכון הבסיס נתונים יום לפני בהפעלה ראשונה
    updated_date=0
    try:
        if not os.path.exists(Consts.lastDate_update_path):
            with open(Consts.lastDate_update_path, "w+") as UPDATE_DATE_FILE:
                updated_date = (datetime.now() - timedelta(days=1)).day
                UPDATE_DATE_FILE.write(str(updated_date))
    except Exception as e:
        print(e, "<<<<<==||| UPDATE_DATE.log can not make new")
        return 0 

    try:
        with open(Consts.lastDate_update_path, "r") as UPDATE_DATE_FILE:
            updated_date = int(UPDATE_DATE_FILE.read())
    except Exception as e:
        print(e, "<<<<<==||| UPDATE_DATE.log cant open the file")
        pass
    return updated_date

    # אם לא קיים מידע בבסיס נתונים אז תעשה עדכון לשליפה מהקבצים
    # or
    # אם התאריך לא מעודכן והשעה אחרי תשע בבוקר אז לעדכן בסיס הנתונים ולעדכן תאריך עדכון
        # (פתיחת האתר הראשונה אחרי השעה 9 יתעדכן הבסיס נתונים)
# קראית המידע ךדף המרכזי
def Is_Update_Needit(updated_date):
    if updated_date > 0 and datetime.now().hour>Consts.update_hour and (not Get_DBJson_Data("PMs.json") or updated_date != datetime.now().day) :
        try:
            with open(Consts.lastDate_update_path, "w+") as UPDATE_DATE_FILE:
                print("+=====> now new day -updating ",updated_date, "->", end=" ")
                updated_date = datetime.now().day
                print(updated_date)
                UPDATE_DATE_FILE.write(str(updated_date))
                return True
        except:pass
    return False

def RUN_Update(ALL_Plant):
    Replace_DBJson_Data("updating_runing.json",{"updating_runing":True})
    for which_plant in ALL_Plant:
        TDC.main_parser(which_plant)
    TDC.Parse_Utils.Update_Pms_Data(ALL_Plant)
    Replace_DBJson_Data("updating_runing.json",{"updating_runing":False})


def Update_Data():
        # if update is runing alrady    
    updating_runing=False
    try:
        updating_runing = Get_DBJson_Data("updating_runing.json")[0]["updating_runing"]
    except Exception as e :return '/update_page'
    if updating_runing:
         return '/wait_update_finsh'
        #check is need to update BY DATE
    updated_date=Get_Last_UpdateDate()
    if updated_date and Is_Update_Needit(updated_date):
        return '/update_page'
    # אם אין נתונים
    MainPage_Data=Get_DBJson_Data("PMs.json")
    if len(MainPage_Data)<1:
         return '/update_page'

    return False