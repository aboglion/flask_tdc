from .Consts import NET, defult_STATUS, PLANT_file_start, NET_B
import os
from .hebrew import fix_if_reversed
from .save_to_db import save_to_db_duplication

def format_number(num):
    try:
        if 0<int(num)<10 :
            return f"0{num}"
        else:
            return str(num)
    except Exception:
        pass
        return num

    
def TAGS_parsing(path, type_):
    all_tags = []
    RETOEN = []
    duplication_all = []
    PLANT = path.split("/")[-2][:2]
    PLANT = list(PLANT_file_start.keys())[
        list(PLANT_file_start.values()).index(PLANT)]
    NET = "B" if PLANT in NET_B else "A"

    # corriction of path in local test files
    if path[:2] == "./":
        path = os.getcwd() + path[1:]
    dctag = {}

    with open(path, "r", encoding='windows-1255') as file:
        text = file.read()
        tags = text.split("{IDF")[1:]
    for tag in tags:
        new_tag = {}  # Create a new dictionary for each iteration
        lines = tag.split("\n")
        DB_FILE = path.split("/")[-1][:-3]
        NAME = lines[2].split()[1]
        new_tag["NAME"] = NAME
        NIM = "######"
        PM = "######"
        CARD = "0"
        PTDESC = "######"
        index = "######"
        for line in lines:
            # אם התג הוא מסוג תוכנה אז דלג על הפרמטרים הל המשתנים של התוכנה
            if not (isWrdsInLine(line, ("NN(", "TIME(", "FL(", "STR8", "STR16", "STR32")) and ("SEQ" in NAME)):
                # Esc the mod params from seq
                words = line.split("=")
                for word, nextword in zip(words, words[1:]):
                    if "$" in word:
                        word = word.replace("$", "")
                    word = word.strip()
                    nextword = nextword.strip()
                    if "NTWKNUM" in word:
                        NIM = nextword
                    if "NODENUM" in word:
                        PM = nextword
                    if "SLOTNUM" in word:
                        index = format_number(nextword)
                    if "MODNUM" in word:
                        CARD = format_number(nextword)
                    if "PTDESC" in word:
                        PTDESC = fix_if_reversed(nextword)
                        # TO MAKE INPOUT DCTAG AND OUT_DC TAG WITH INDEX IN CARD ADRI..
                    if type_ == "DC" and (("DISRC(" in word and "!" in nextword) or ("DODSTN(" in word and ".SO" in nextword)):
                        dctag = {}
                        dctag["TYPE"] = word[:2]
                        dctag["NAME"] = f"{NAME} [DC-{dctag['TYPE']}]"
                        dc_card = format_number(nextword[3:5])
                        ds_index = format_number(nextword[6:8])
                        dctag["DC_index"] = ds_index
                        if dc_card == "######":
                            dc_card = type_
                        dctag["DB_FILE"] = DB_FILE
                        dctag["CARD_ID"] = "-".join([NET, NIM, PM, dc_card])
                        dctag["ID"] = "-".join([NET, NIM,
                                               PM, dc_card, ds_index])
                        dctag["STATUS"] = defult_STATUS
                        dctag["PLANT"] = PLANT
                        dctag["PTDESC"] = PTDESC
                        dctag["SLOTNUM"] = ds_index
                        dctag["NODENUM"] = PM

                        all_tags.append(dctag)

                    new_tag[word] = nextword
                    new_tag["PTDESC"] = PTDESC
            new_tag["DB_FILE"] = DB_FILE
            new_tag["CARD_ID"] = "-".join([NET, NIM, PM, CARD])
            new_tag["ID"] = "-".join([NET, NIM, PM, CARD, index])
            new_tag["STATUS"] = defult_STATUS
            new_tag["TYPE"] = type_
            new_tag["PLANT"] = PLANT

        for i in ["DISRC(1)", "DISRC(2)", "DODSTN(1)", "DODSTN(2)", "CODSTN(1)", "CISRC(1)", "CISRC(2)", "PVSRCOPT"]:
            if not new_tag.get(i):
                new_tag[i] = " --- "
        if new_tag.get('PNTMODTY') == "LLMUX":
            new_tag["TYPE"] = "LLMUX"

        if new_tag["TYPE"] == "RC" and "!AO" in new_tag["CODSTN(1)"] and ".OP" in new_tag["CODSTN(1)"]:
            index = format_number(new_tag["CODSTN(1)"].split(".")[0][-2:])
            # print(index)
            # print("the old -->","card:",new_tag["CARD_ID"] ,"id:", new_tag["ID"])
            new_tag["CARD_ID"] = "-".join([NET,
                                          NIM, PM, format_number(new_tag["CODSTN(1)"][3:5])])
            new_tag["ID"] = new_tag["CARD_ID"]+"-"+index
            # print("the new -->","card:",new_tag["CARD_ID"], "id:", new_tag["ID"],"\n===================\n\n")
        try:
            with open('templates/duplication.html', 'a', encoding="utf-8") as file:
                # בדיקה אם יש כפליות של כתובת בבסיס הנתונים
                for tag_index in all_tags:
                    if tag_index["ID"] == new_tag["ID"]:
                        duplication_ = {
                            "PLANT": PLANT,
                            "ADDRESS": new_tag["ID"],
                            "NAME1": tag_index["NAME"],
                            "DB_FILE1": tag_index["DB_FILE"],
                            "TYPE1": tag_index["TYPE"],
                            "NAME2": new_tag["NAME"],
                            "DB_FILE2": new_tag["DB_FILE"],
                            "TYPE2": new_tag["TYPE"]
                        }
                        save_to_db_duplication(duplication_)
        except Exception  as e:pass
        all_tags.append(new_tag)

    RETOEN.extend(all_tags)
    return RETOEN


def isWrdsInLine(line, list):
    for w in list:
        if w in line:
            return True
    return False
