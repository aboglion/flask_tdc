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


def RUN_Update(ALL_Plant):
    for which_plant in ALL_Plant:
        TDC.main_parser(which_plant)
    TDC.Parse_Utils.Update_Pms_Data(ALL_Plant)
    with open(Consts.lastDate_update_path, "w+") as UPDATE_DATE_FILE:
        UPDATE_DATE_FILE.write(str(datetime.now().day))
    return False



def Update_Data():
        # if update is runing alrady  
        #   
    updating_runing=False
    try:
        updating_runing = Get_DBJson_Data("updating_runing.json")
        if updating_runing and updating_runing[0]:
            updating_runing=updating_runing[0]["updating_runing"]
        else:
            return False
    except Exception as e :
        print("Update_Data() err :", e)
        return f'Update_Data() err : {e}'
    if updating_runing:
         print("wait_update_finsh")
         return '/wait_update_finsh'
    return False
