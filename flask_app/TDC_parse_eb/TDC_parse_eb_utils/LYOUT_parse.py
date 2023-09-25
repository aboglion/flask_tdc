import os
from .Consts import lyout_sizes


def LYOUT_parse(path, tags):
    Invalid = []

    lyout = {}

    # המרת הנתיב למחרוזת
    str_path = str(path)
    
    # קריאה של הקובץ למשתנה text
    with open(str_path, "r") as file:
        text = file.read()

    # בדיקה אם הנתיב התחיל ב"./" ואז עדכון שלו
    if str_path[:2] == "./":
        path = os.path.join(os.getcwd(), str_path[2:])

    # השגת השם של המתקן מהנתיב
    PLANT = str_path[-10:-7]

    lines = text.split("\n")
    PM, CARD, TYPE = 0, 0, 0

    # עיבוד השורות מהקובץ
    for line in lines:
        words = line.split(" = ")
        for word, nextword in zip(words, words[1:]):
            if "NODENUM" in word:
                PM = nextword
            if "IOMFILEA" in word:
                CARD = word.split("(")[1][:-1]
            if "IOMTYPE" in word:
                TYPE = nextword.strip()
        
        # עדכון המטרציה lyout בהתאם למידע שנמצא
        if TYPE:
            if PLANT not in lyout:
                lyout[PLANT] = {}
            if PM not in lyout[PLANT]:
                lyout[PLANT][PM] = {}
            if CARD not in lyout[PLANT][PM]:
                lyout[PLANT][PM][CARD] = [{"TYPE": TYPE, "PM": PM, "CARD_NUM": int(CARD)} for _ in range(lyout_sizes[TYPE])]
                CARD, TYPE = 0, 0

    # עיבוד התגים
    for tag in tags:
        # דלג על כל התגים שיש להם הסימן דולר כיוון שאלה תגים של הגדרות מערכת 
        if tag["NAME"][0] == "$":
            continue
        # אם הכתובת של התג מכילה כרטיס 0 זאת אומרת שזה לא תג פיזי אלא תג תוכנתי
        # יש לדלג אין לו כתובת פיזית בבקר
        tag_id = tag["ID"].split("-")
        if tag_id[-2] == "0":
            continue
        try: #  (הבקר והכרטיס) תנסה להוציא את הכתובת 
            if not len(tag_id):
                raise Exception
            tag_pm = "{:02d}".format(int(tag_id[-3]))
            tag_card = str(int(tag_id[-2]))
        except Exception:
            Invalid.append(f"\nInvalid tag :\n {tag} {'-' * 20}")
            continue  # דילוג על התג הזה והמשך לבדיקה של התג הבא אם הוצאת הנתונים נכשלה 
        try: #   תכניס את התג 
            tag_position = int(tag_id[-1]) - 1 # המיקום בכרטיס
            if not tag_card == '0':
                lyout[PLANT][str(tag_pm)][tag_card][tag_position]["NAME"] = tag["NAME"]
                lyout[PLANT][str(tag_pm)][tag_card][tag_position]["STATUS"] = tag["STATUS"]
                lyout[PLANT][str(tag_pm)][tag_card][tag_position]["POINT_NUM"] = int(tag["ID"].split("-")[-1])
                lyout[PLANT][str(tag_pm)][tag_card][tag_position]["CARD_ID"] = tag["CARD_ID"]
        except Exception:
            print("\n\n\n---------======\n", tag["NAME"], tag_position, len(lyout[PLANT][str(tag_pm)][tag_card]))

    # החזרת המילון lyout והשגיאות
    return [lyout, {"errors": Invalid}]
