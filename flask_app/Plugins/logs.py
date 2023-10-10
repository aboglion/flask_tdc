from glob import glob
import TDC_parse_eb.TDC_parse_eb_utils.Consts as Consts
import os,datetime
from .DBJson import load_all_log_entries,append_log_entry

# LOGS

def Get_DbLogs_Dates():
    #  בשביל להציג בדף ראשי מצב עדכון קבצים : שליפת הקבצים של הלוג תאריכי עדכוני השלבים מהתקייה
    # גזירת השם של הקובץ מהנתיב
    # מיון לכל רשת את הקבצים שלה
    dates_reports_file_pathes = glob(f'{Consts.EB_FILES_DIR}/../Rep/*.ADATE')
    dates_reports_files, dates_reports_files_A, dates_reports_files_B = [], [], []
    for path in dates_reports_file_pathes:
        dates_reports_files.append(path.split("/")[-1].split(".")[0])
        if (dates_reports_files[-1][0] == "A"):
            dates_reports_files_A.append(dates_reports_files[-1])
        if (dates_reports_files[-1][0] == "B"):
            dates_reports_files_B.append(dates_reports_files[-1])
    return {"A":dates_reports_files_A,"B":dates_reports_files_B}




def log_user_entry():
    username = os.getlogin()
    now = str(datetime.datetime.now().replace(second=0, microsecond=0))
    new_log_entry = {"name": username, "time": now}
    all_entries = load_all_log_entries('log_entries.json')
    if not(len(all_entries)>0 and all_entries[-1]==new_log_entry):
        append_log_entry(new_log_entry, 'log_entries.json')

