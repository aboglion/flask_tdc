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
    the_new_dic_ids = {item['ID']: item for item in parse_EB_DATA}
    # print(parse_dict)
    ii = 0
    for old in DB_DATA:
        courcting_num_id_num=old["ID"].split("-")[-1]
        courcting_num_id_card=old["ID"].split("-")[-2:-1]
        if len(courcting_num_id_num)>=2 and courcting_num_id_num[0]=="0":
            courcting_num_id_num=courcting_num_id_num[1:]
            old["ID"]="-".join(old["ID"].split("-")[:-1],courcting_num_id_num)
        if len(courcting_num_id_card)>=2 and courcting_num_id_card[0]=="0":
            courcting_num_id_card=courcting_num_id_card[1:]
            old["ID"]="-".join(old["ID"].split("-")[:-2],courcting_num_id_card,courcting_num_id_num)            
        # ביצוע חיפוש לפי המזהה (ID) במילון במקום לסנן את הרשימה
        if old["ID"] not in the_new_dic_ids:
            if old["STATUS"] == "EXISTED":
                old["STATUS"] = "DELETED"
            UPDATED.append(old)
    parse_EB_DATA.extend(UPDATED)
    TAGS_DB.close()
    return parse_EB_DATA
