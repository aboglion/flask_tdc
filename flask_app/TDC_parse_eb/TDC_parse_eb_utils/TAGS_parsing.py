from .Consts import NET, defult_STATUS, PLANT_file_start, NET_B
import os
from .hebrew import fix_if_reversed
from .save_to_db import save_to_db_duplication

def format_number(num):
    try:
        num_int = int(num)
        if 0 < num_int < 10:
            return f"0{num_int}"
        else:
            return str(num_int)
    except ValueError:
        return str(num)

def TAGS_parsing(path, type_):
    all_tags = []
    RETOEN = []
    duplication_all = []
    PLANT = path.split("/")[-2][:2]
    PLANT = list(PLANT_file_start.keys())[list(PLANT_file_start.values()).index(PLANT)]
    NET = "B" if PLANT in NET_B else "A"

    # Correcting the path in local test files
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
        NIM, PM, CARD, PTDESC, index = "######", "######", "0", "######", "######"
        
        for line in lines:
            if not (isWrdsInLine(line, ("NN(", "TIME(", "FL(", "STR8", "STR16", "STR32")) and ("SEQ" in NAME)):
                words = line.split("=")
                for word, nextword in zip(words, words[1:]):
                    word = word.strip().replace("$", "")
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
                    if type_ == "DC" and (("DISRC(" in word and "!" in nextword) or ("DODSTN(" in word and ".SO" in nextword)):
                        dctag = {
                            "TYPE": word[:2],
                            "NAME": f"{NAME} [DC-{word[:2]}]",
                            "DB_FILE": DB_FILE,
                            "CARD_ID": "-".join([NET, NIM, PM, format_number(nextword[3:5])]),
                            "ID": "-".join([NET, NIM, PM, format_number(nextword[3:5]), format_number(nextword[6:8])]),
                            "STATUS": defult_STATUS,
                            "PLANT": PLANT,
                            "PTDESC": PTDESC,
                            "SLOTNUM": format_number(nextword[6:8]),
                            "NODENUM": PM
                        }
                        all_tags.append(dctag)
                    new_tag[word] = nextword
                    new_tag["PTDESC"] = PTDESC
        
        new_tag.update({
            "DB_FILE": DB_FILE,
            "CARD_ID": "-".join([NET, NIM, PM, CARD]),
            "ID": "-".join([NET, NIM, PM, CARD, format_number(index)]),
            "STATUS": defult_STATUS,
            "TYPE": type_,
            "PLANT": PLANT
        })
        
        for i in ["DISRC(1)", "DISRC(2)", "DODSTN(1)", "DODSTN(2)", "CODSTN(1)", "CISRC(1)", "CISRC(2)", "PVSRCOPT"]:
            if not new_tag.get(i):
                new_tag[i] = " --- "
        
        if new_tag.get('PNTMODTY') == "LLMUX":
            new_tag["TYPE"] = "LLMUX"

        if new_tag["TYPE"] == "RC" and "!AO" in new_tag["CODSTN(1)"] and ".OP" in new_tag["CODSTN(1)"]:
            index = format_number(new_tag["CODSTN(1)"].split(".")[0][-2:])
            new_tag["CARD_ID"] = "-".join([NET, NIM, PM, format_number(new_tag["CODSTN(1)"][3:5])])
            new_tag["ID"] = f"{new_tag['CARD_ID']}-{index}"

        try:
            with open('templates/duplication.html', 'a', encoding="utf-8") as file:
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
        except Exception as e:
            pass
        
        all_tags.append(new_tag)

    RETOEN.extend(all_tags)
    return RETOEN

def isWrdsInLine(line, word_list):
    for w in word_list:
        if w in line:
            return True
    return False
