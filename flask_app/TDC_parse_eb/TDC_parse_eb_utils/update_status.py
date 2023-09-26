from tinydb import TinyDB
from .Consts import DB_JASON

# פונקציה לעדכון מצב (סטטוס) של נתונים מסוימים בעץ המידע
def update_status(parse_EB_DATA, which_plant):
    TAGS_DB = TinyDB(f'{DB_JASON}/TAGS_DB_{which_plant}.json')
    UPDATED = []
    try:
        DB_DATA = TAGS_DB.all()[0].get(which_plant, [])
    except:
        print(f"קובץ מידע JSON של {which_plant} חסר")
        return parse_EB_DATA
    # המרת parse_EB_DATA למילון לצורך חיפוש מהיר יותר
    parse_dict = {item['ID']: item for item in parse_EB_DATA}
    # print(parse_dict)
    ii = 0
    for i in DB_DATA:
        # ביצוע חיפוש לפי המזהה (ID) במילון במקום לסנן את הרשימה
        if i["ID"] not in parse_dict:
            if i["STATUS"] == "existed":
                i["STATUS"] = "deleted"
            UPDATED.append(i)
    parse_EB_DATA.extend(UPDATED)
    TAGS_DB.close()
    return parse_EB_DATA