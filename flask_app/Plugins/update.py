from datetime import datetime, timedelta
from tinydb import TinyDB, Query
import TDC_parse_eb.TDC_parse_eb as TDC
import TDC_parse_eb.TDC_parse_eb_utils.Consts as Consts


# UPDATE

def Get_Last_UpdateDate():
    # תאריך עדכון הבסיס נתונים יום לפני בהפעלה ראשונה
    try:
        with open(f'./TDC_parse_eb/UPDATE_DATE.log', "r") as UPDATE_DATE_FILE:
            updated_date = int(UPDATE_DATE_FILE.read())
    except Exception as e:
        print(e, "<<<<<==||| UPDATE_DATE.log no file")
        with open(f'./TDC_parse_eb/UPDATE_DATE.log', "w+") as UPDATE_DATE_FILE:
            updated_date = (datetime.now() - timedelta(days=1)).day
        UPDATE_DATE_FILE.write(str(updated_date))
        pass
    return updated_date

    # אם לא קיים מידע בבסיס נתונים אז תעשה עדכון לשליפה מהקבצים
    # or
    # אם התאריך לא מעודכן והשעה אחרי תשע בבוקר אז לעדכן בסיס הנתונים ולעדכן תאריך עדכון
        # (פתיחת האתר הראשונה אחרי השעה 9 יתעדכן הבסיס נתונים)
# קראית המידע ךדף המרכזי
def Is_Update_Needit(data_main,updated_date):
    if not data_main or updated_date != datetime.now().day:
        with open(f'./TDC_parse_eb/UPDATE_DATE.log', "w+") as UPDATE_DATE_FILE:
            print("+=====> now new day -updating ",
                  updated_date, "->", updated_date, end=" ")
            updated_date = datetime.now().day
            print(updated_date)
            print(bool(data_main))
            UPDATE_DATE_FILE.write(str(updated_date))
            PMs_DB = TinyDB(f'{Consts.DB_JASON}/PMs.json')
            data_main = PMs_DB.all()
            PMs_DB.close()
            return True
    return False

def RUN_Update(ALL_Plant):
    for which_plant in ALL_Plant:
        TDC.main_parser(which_plant)
    TDC.Parse_Utils.Update_Pms_Data(ALL_Plant)
