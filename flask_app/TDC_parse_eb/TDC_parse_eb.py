import glob
import os
from pathlib import Path
from dotenv import dotenv_values  # install python-dotenvto_db
import TDC_parse_eb.TDC_parse_eb_utils as Parse_Utils
import TDC_parse_eb.TDC_parse_eb_utils.Consts as Consts


# פונקציה ראשית לעיבוד המידע
def main_parser(which_plant,which_pm='*', which_type='*'):
    which_pm = "PM" + which_pm

    # בדיקת סוג הנתונים אם קיים
    if which_type not in Consts.TAGS_TYPE:
        print(f"the type must be in {Consts.TAGS_TYPE}")
        return
    print(f'{which_plant} now started')

    # בודק אם שם המתקן קיים ברשימת המתקנים המוגדרים כקבועים
    if which_plant not in Consts.PLANT_file_start:
        print(f"the plant name must be in {Consts.PLANT_file_start.keys()}")
        return
    # מציאת תקיית המתקן  בפרויקט (כלול בקבוע Consts.PLANT_file_start)
    PLANT_FOLDERS = glob.glob(
        f'{Consts.EB_FILES_DIR}/{Consts.PLANT_file_start[which_plant]}BC', recursive=True)
    if not PLANT_FOLDERS:
        print(
            f"{which_pm} !-->missed folder EC : {Consts.EB_FILES_DIR}/{Consts.PLANT_file_start[which_plant]}BC")
        return
    # כניסה ל  קבצים בתקייה
    for folder in PLANT_FOLDERS:
        # הוצאת שם המתקן הנוכחי מתוך השם של התקייה שלו
        current_plant = next(
            (i for i in Consts.PLANT_file_start if Consts.PLANT_file_start[i] == folder[-4:-2]), None)
        #  ucn_file בניית שם קובץ UCN.EB עבור המתקן הנוכחי
        # זהו קובץ מיוחד שיש בו כל המפה הכללית של הכרטיסים והגדלים של כל כרטיס והסוג שלו
        ucn_file = Path(folder) / f"{current_plant}_UCN.EB"
        # tags_files שאר הקבצים הם קבצים של תגים
        tags_files = glob.glob(
            str(Path(folder) / f'{which_pm}{which_type}*.EB'))
        # אם אין קבצים EB
        if not (tags_files and ucn_file):
            print(
                f"{which_pm} !-->missed EB FILE: IN THER IS NO DATA FOR {which_pm} IN PLANT {current_plant}")
            return

        # רשימה לאחסון הנתונים מהקבצים ה-EB
        tags_ = []
        # לעבור על כל קובץ EB ולעבוד עליו
        for index, file_path in enumerate(tags_files):
            progress = (index + 1) / len(tags_files) * 100
            print(f'{current_plant}: now {progress:.2f}%')

            # אם הסוג הוא "*" (כל הסוגים), נבדוק את הסוג מתוך שם הקובץ
            if which_type == "*":
                file_name = Path(file_path).name
                current_type = file_name[4:6] if file_name[6] in [
                    ".", "_"] else file_name[4:7]
            else:
                # אם הסוג מוגדר באופן ספציפי, נשתמש בו
                current_type = which_type

            # Parse_Utils.TAGS_parsing -->הפונקציה שמוציאה את כל הנתונים מהקבצים
            # הוספת הנתונים מהקובץ ה-EB לרשימה
            tags_.extend(Parse_Utils.TAGS_parsing(file_path, current_type))

        try:
            # אם ישנם נתונים ברשימת ה-TAGS
            if tags_:
                #     Parse_Utils.update_status פונקציה לעדכון מצב
                #     אם הקובץ קיים בישן ולא קיים בוצאה החדשה אז הוא נמחק מקבל סטטוס מחוק
                # עדכון מצב (סטטוס) של נתונים על פי מה שנמצא בבסיס הנתונים
                tags_ = Parse_Utils.update_status(tags_, current_plant)

                # LYOUT קריאה לפונקציה לעיבוד ושמירת ה-Parse_Utils.LYOUT_parse
                # LYOUT שזה בעצם הכנת מערך דו מימדי לטבלה של ה
                LYOUT, Invalid_LYOUT = Parse_Utils.LYOUT_parse(ucn_file, tags_)
            else:
                print(f"err in db file of {current_plant}")

            # שמירה במסדי נתונים (DB)
            Parse_Utils.save_to_db(current_plant,tags_, LYOUT, Invalid_LYOUT)
        except UnboundLocalError as e:
            print(e)
            print(f"LYOUT ERROR IN {current_plant}")
            continue

