# DBJson

from tinydb import TinyDB
import json,os
import TDC_parse_eb.TDC_parse_eb_utils.Consts as Consts


def Get_DBJson_Data(json_file):
    try:
        DBJson = TinyDB(f'{Consts.DB_JASON}/{json_file}')
        DBJson_Data = DBJson.all()
        DBJson.close()
        return DBJson_Data
    except Exception as e:
        print("there is no page data file", f'{e},{Consts.DB_JASON}/{json_file}')
        return False


def Replace_DBJson_Data(jasonfile,newdata):
        DB = TinyDB(f'{Consts.DB_JASON}/{jasonfile}')
        DB.truncate()
        DB.insert(newdata)
        DB.close


def Filtered_Sarch(ALL_Plant, varibles_for_search):
    #PLANT FILTER------[1]-----
        # בדיקת אם המתקן נמצא במילון החיפוש
    # יבוא מידע רק של המתקן הספיציי
    if "PLANT" in varibles_for_search:  # אם הוגדר מתקן ספציפי
        which_plant = varibles_for_search['PLANT']
        if not which_plant in ALL_Plant:  # לבדוק אם לא הכניסו סתם שם של מתקן הכתובת
            return []
        else:
            search_on_plant = [which_plant]
    else:
        search_on_plant = ALL_Plant  # אם לא הוגדר מתקן ספציפי
    # varibles_for_search get from url and clean empty ,to filterat keys data


    re = []
    name = False   # אם יש חיפוש על השם
    desc = False  # אם יש חיפוש על דיסקרפשן
    # NAME  FILTER------[2]-----
    if "NAME" in varibles_for_search:  # השם והדיסקרפשין לא רוצים לפלטר במדויק לכן נשמרים על נמנת לעשות חיפוש על חלק מהמילה ולא המילה המדוייקת
        name = varibles_for_search["NAME"]
        del varibles_for_search["NAME"]

    # PTDESC (DESCRPTIONS) FILTER------[3]-----
    if "PTDESC" in varibles_for_search:
        desc = varibles_for_search["PTDESC"]
        del varibles_for_search["PTDESC"]

    ##SEARCHING in Plant [1]
    for which_plant in search_on_plant:
        DATA =Get_DBJson_Data(f'TAGS_DB_{which_plant}.json')
        if len(DATA) > 0:
            TAGS_DATA = DATA[0][which_plant]
            # במדויק -אם הערכים לחיפוש נמצאים אז לפלטר רק את הנתונים שיש להן אותם
            
            # אם נשאר עוד אלמנטים לפלטר אז לכנס למתקנים\מתקן ולפלטר את הכל ולהחזיר מתקן מפולטר
            if (varibles_for_search):
                result = []
                for item in list(TAGS_DATA):
                    if all(item.get(key) == value for key, value in varibles_for_search.items()):
                        result.append(item)
            re.extend(result)
        else:
            continue

    #   חיפוש בשם ותיאור 
    # re = חיפוש חלק מהמילה - ריגולר אקספרשן
    if name:
     # הכנס אליו את האיברים שיש להם דיסקרפשין שחלק ממנו נמצא אם לא נמצא החזר ריק
        re = [d for d in re if name in d.get("NAME", "")]

    if desc:
        # הכנס אליו את האיברים שיש להם דיסקרפשין שחלק ממנו נמצא אם לא נמצא החזר ריק
        re = [d for d in re if desc in d.get("PTDESC", "")]
    return re



def Update_DBJson_Data(it):
    try:
        lyputpm = '0'+it["PM"] if len(it["PM"]) < 2 else it["PM"]
        plant=it["PLANT"]
    except :return (f"NO PM OR PLANT IN {it}")

    #להוציא את שמות בסיס הנתונים של המתקן 
    LYOUT_JASON_FILE=f'LYOUT_DB_{plant}.json'
    TA_DB_FILE=f'TAGS_DB_{plant}.json'

#שליפת בסיס הנתונים ושינוי הערך הרצוי שם
    LYOUT_DATA=Get_DBJson_Data(LYOUT_JASON_FILE)[0]
    try:LYOUT_DATA[it["PLANT"]][lyputpm][str(it["CARD_NUM"])][int(it["POINT_NUM"])-1] = it
    except Exception as e:
        return (e,f' sorry can not update LYOUT \n {it}')
    
    Replace_DBJson_Data(LYOUT_JASON_FILE,LYOUT_DATA)

    try:tags=Get_DBJson_Data(TA_DB_FILE)[0][plant]
    except:return (f'can not find {plant} in the DB data')
    
    #make s_t new on without the old tag
    s_t = [t for t in tags if t["ID"] != it["ID"]]
    s_t.append(it) # add the new tag
    
    Replace_DBJson_Data(TA_DB_FILE,{it["PLANT"]: s_t})


def save_log_entry(entry, filename):
    with open(f'{Consts.DB_JASON}/{filename}', 'w') as file:
        json.dump(entry, file)

def load_log_entry(filename):
    try:
        with open(f'{Consts.DB_JASON}/{filename}', 'r') as file:
            entry = json.load(file)
        return entry
    except FileNotFoundError:
        return None



def append_log_entry(entry, filename):
    filename = os.path.join(Consts.DB_JASON, filename)  # Assuming Consts.DB_JASON is the correct path
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                log_entries = json.load(file)
        else:
            log_entries = []
    except json.decoder.JSONDecodeError:
        log_entries = []

    log_entries.append(entry)

    with open(filename, 'w') as file:
        json.dump(log_entries, file)


def load_all_log_entries(filename):
    filename = os.path.join(Consts.DB_JASON, filename)  # Assuming Consts.DB_JASON is the correct path

    try:
        with open(filename, 'r') as file:
            log_entries = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        log_entries = []

    return log_entries
