from glob import glob
import TDC_parse_eb.TDC_parse_eb_utils.Consts as Consts


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

