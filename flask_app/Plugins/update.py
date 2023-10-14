from datetime import datetime, timedelta
from tinydb import TinyDB, Query
import TDC_parse_eb.TDC_parse_eb as TDC
import os
from .DBJson import Replace_DBJson_Data

# UPDATE

def Get_Last_UpdateDate():
    # תאריך עדכון הבסיס נתונים יום לפני בהפעלה ראשונה
    updated_date=0
    lastDate_update='./TDC_parse_eb/UPDATE_DATE.log'
    try:
        if not os.path.exists(lastDate_update):
            with open(lastDate_update, "w+") as UPDATE_DATE_FILE:
                updated_date = (datetime.now() - timedelta(days=1)).day
                UPDATE_DATE_FILE.write(str(updated_date))
    except Exception as e:
        print(e, "<<<<<==||| UPDATE_DATE.log can not make new")
        return 0 

    try:
        with open(lastDate_update, "r") as UPDATE_DATE_FILE:
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
def Is_Update_Needit(data_main,updated_date):
    if updated_date >0 and (not data_main or updated_date != datetime.now().day) :
        with open(f'./TDC_parse_eb/UPDATE_DATE.log', "w+") as UPDATE_DATE_FILE:
            print("+=====> now new day -updating ",
                  updated_date, "->", updated_date, end=" ")
            updated_date = datetime.now().day
            print(updated_date)
            UPDATE_DATE_FILE.write(str(updated_date))
            return True
    return False

def RUN_Update(ALL_Plant):
    Replace_DBJson_Data("updating_runing.json",{"updating_runing":True})
    for which_plant in ALL_Plant:
        TDC.main_parser(which_plant)
    TDC.Parse_Utils.Update_Pms_Data(ALL_Plant)
    Replace_DBJson_Data("updating_runing.json",{"updating_runing":False})

