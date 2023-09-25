from .Consts import PLANT_LETTER,NET_B
import os
from glob import glob
from tinydb import TinyDB



all_plants = {}
LYOUT=glob("./DB/LYOUT_DB_*.json")
print(LYOUT,"--")

# יצירת דף ראשי( סטטיסטיקה + תפריט )לכל המתקןים
def Update_Pms_Data():
    plant_list=[]
    for p in LYOUT:
        if os.path.getsize(p) > 0:
            plant=p[:-5].split("_")[-1]# ./DB/LYOUT_DB_651.json
            plant_list.append(plant)
    print(plant_list)
    all={}
    # for plant in ["800"]:
    for plant in plant_list:
        try:
            LYOUT_DB = TinyDB(f'./DB/LYOUT_DB_{plant}.json')
            PMs_DATA=LYOUT_DB.all()[0][plant]
            LYOUT_DB.close()
        except Exception as e:
            print(e,"\n Update_Pms_Data NO ./DB/LYOUT_DB_{plant}.json FILE")
        pms=[]
        for pm in PMs_DATA:
            pm_=f'{pm}'
            sub_is_done=False
            L={pm_:{"AO":[0,0],"AI":[0,0],"DI":[0,0],"DO":[0,0],"LLMUX":[0,0],"ELSE":[0,0]}}
            CONTER=0
            for card in PMs_DATA[pm_]:
                card_=PMs_DATA[pm_[:2] if sub_is_done else pm_][card]
                if len(card_)>0:
                    TYPE=card_[0]["TYPE"]
                    if "AO" in TYPE:TYPE="AO"
                    elif "AI" in TYPE:TYPE="AI"
                    elif "DI" in TYPE:TYPE="DI"
                    elif "DO" in TYPE:TYPE="DO"
                    elif "LLMUX" in TYPE:TYPE="LLMUX"
                    else: TYPE="ELSE"

                    LEN=len(card_)
                    for point in card_:
                        if not point.get("NAME")==None :
                            CONTER+=1
                            if plant==("630") and not sub_is_done:
                                F_LEETER= point["NAME"][0]
                                sub_plant = next((k for k, v in PLANT_LETTER.items() if v == F_LEETER), None)
                                sub_plant=f"{pm_}</p><p>LEETER:[{F_LEETER}]</p><p>Sub Plant:[{sub_plant}]"
                                L[sub_plant] = L[pm_]
                                del L[pm_]
                                pm_=sub_plant
                                sub_is_done=True
                    L[pm_][TYPE][0]+=CONTER
                    L[pm_][TYPE][1]+=LEN
                    CONTER=0
            pms.append(L)
                    # print(pm_,TYPE,CONTER,"/",LEN)
        pms.append(PLANT_LETTER[plant])
        pms.append("B" if plant in NET_B else "A")
        all[plant]=pms
        pms=[]
    PMs_DB = TinyDB(f'./DB/PMs.json')
    PMs_DB.truncate()
    PMs_DB.insert(all)
    PMs_DB.close()