import os
import time
import glob
from tinydb import TinyDB, Query
from shutil import copytree, rmtree, ignore_patterns
from TDC_parse_eb.TDC_parse_eb_utils.Consts import DB_JASON, plant_map, EB_FILES_DIR, epks
from TDC_parse_eb.TDC_parse_eb_utils.hebrew import fix_if_reversed


def find_data(tag, data):
    for i in data:
        if i['ENTITY'] == tag:
            return i
    return False

# Define the paths for different entities
paths = {
    "A": f'{EB_FILES_DIR}/../Rep/PVSRC_A.XX',
    "B": f'{EB_FILES_DIR}/../Rep/PVSRC_B.XX'
}

today_ = time.strftime("%d-%b-%Y", time.gmtime())
date_files = {"A": " ", "B": " "}



def pvsrc_parse():
    # Initialize the TinyDB database and table
    PVSRC_HISTORY_DB = TinyDB(DB_JASON+'/PVSRC_HISTORY_DB.json')
    PVSRC_TODAY_DB = TinyDB(DB_JASON+'/PVSRC_TODAY_DB.json')
    PVSRC_LAST_DB = TinyDB(DB_JASON+'/PVSRC_LAST_DB.json')
    # Get the existing data from the TinyDB database
    HISTORY_DATA = PVSRC_HISTORY_DB.all()
    LAST_DATA = PVSRC_LAST_DB.all()
    TODAY_DATA = PVSRC_TODAY_DB.all()
    TAG = Query()
    # Read data from the files and update the database and TreeView
    try:
        data = []
        for NET in ["A", "B"]:
            startline = 3 if data else 2
            datastring = open(paths[NET], "r", encoding='windows-1255').read().splitlines()[startline:]
            for l in datastring:
                l = l.split()
                if len(l) > 3:
                    if "ERRORS" in l[0] or "Request" in l[0]:
                        continue
                    ENTITY = f"{plant_map[l[0][0]]} => {l[0]}"
                    PVSOURCE = l[1]
                    PTDESC = " ".join(l[2:])
                    PTDESC = fix_if_reversed(PTDESC)

                    data.append({"ENTITY": ENTITY, "PVSOURCE":"SOURCE => ALL" if PVSOURCE=="AUTO" else PVSOURCE,
                                "PTDESC": PTDESC, "REASON": ""})
        # exprian files =-=-=============================================
        epks_file_list = glob.glob(epks)
        if len(epks_file_list) > 0:
            epks_file_list = sorted(
                epks_file_list, key=lambda x: os.path.getmtime(x), reverse=True)
            newest_files = epks_file_list[:2]
        for epks_file in epks_file_list:
            startline = 2
            datastring = open(
                epks_file, "r", encoding='windows-1255').read().splitlines()[startline:]

            mitkan_epks = epks_file.split("\\")[1].split(" ")[0]
            for l in datastring:

                l = l.split(",")
                if len(l) > 3:
                    if "ERRORS" in l[0] or "Request" in l[0]:
                        continue
                    ENTITY = f"{mitkan_epks} => {l[0]}"
                    PVSOURCE = l[1]
                    PTDESC = " ".join(l[2:])
                    data.append(
                        {"ENTITY": ENTITY, "PVSOURCE": PVSOURCE, "PTDESC": PTDESC, "REASON": ""})

        for t in LAST_DATA:
            if (t["ENTITY"] in data):
                print(t["ENTITY"])
    except Exception as e:
        print(e, "EXPRINA ERR")
        pass

    if len(TODAY_DATA) == 0:
        PVSRC_TODAY_DB.insert_multiple(data)

    # Extract 'ENTITY' values from both dictionaries
    entities_data = [[item['ENTITY'],[item['PVSOURCE']]] for item in data]
    entities_LAST_DATA = [[item['ENTITY'],[item['PVSOURCE']]] for item in LAST_DATA]

    # Find entities in dect1 that are not in dect2
    not_in_LAST_DATA = [entity for entity in entities_data if entity not in entities_LAST_DATA]

    # Find entities in dect2 that are not in dect1
    not_in_data = [entity for entity in entities_LAST_DATA if entity not in entities_data]

    in_last_day = [entity for entity in entities_data if entity in entities_LAST_DATA]
    print("not_in_LAST_DATA", not_in_LAST_DATA)
    print("--------------------------\n"*2)
    print("not_in_data", not_in_data)
    print("--------------------------\n"*2)
    print("in_last_day", in_last_day)
    print("--------------------------\n"*2)

    if not_in_LAST_DATA:
        for entityarry in not_in_LAST_DATA:
            entity=entityarry[0]
            tag_new = PVSRC_TODAY_DB.search(TAG["ENTITY"] == entity)
            if len(tag_new) == 0:
                tag = (find_data(entity, data))
                PVSRC_TODAY_DB.insert(tag)
            PVSRC_TODAY_DB.update({"START_AT": today_, "NEW": True}, TAG["ENTITY"] == entity)

    if not_in_data:
        for entityarry in not_in_data:
            entity=entityarry[0]
            e = PVSRC_LAST_DB.search(TAG["ENTITY"] == entity)
            e[0].update({"END_AT": today_})
            e[0].pop("NEW", None)
            PVSRC_HISTORY_DB.insert(dict(e[0]))
            tag_his = PVSRC_TODAY_DB.search(TAG["ENTITY"] == entity)
            if len(tag_his) > 0:
                print("\n removed ", tag_his)
                PVSRC_TODAY_DB.remove(TAG["ENTITY"] == entity)

    if in_last_day:
        for entityarry in in_last_day:
            entity=entityarry[0]
            tag_t = PVSRC_TODAY_DB.search(TAG["ENTITY"] == entity)
            tag_old_date = PVSRC_LAST_DB.search(TAG["ENTITY"] == entity)[-1]["START_AT"]
            if len(tag_t) > 0:
                PVSRC_TODAY_DB.update({"START_AT": tag_old_date, "NEW": None}, TAG["ENTITY"] == entity)
    
    TODAY_DATA = PVSRC_TODAY_DB.all()
    PVSRC_LAST_DB.truncate()
    PVSRC_LAST_DB.insert_multiple(TODAY_DATA)

    PVSRC_LAST_DB.close()
    PVSRC_TODAY_DB.close()
    PVSRC_HISTORY_DB.close()
