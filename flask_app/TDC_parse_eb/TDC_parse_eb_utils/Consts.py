
import os
defult_STATUS = "EXISTED"

# ####-====== RUN MODE TOGALS .. =====
####[1]-- BYCcompose  http://localhost --
EB_FILES_DIR="/TDC/DB"
DB_JASON="/TDC/DB_JASON"
DB_SQL="/TDC/DB_SQL"   # the folder
def runmode(app):
    print("SERVER RUNING")

#####[2]-- debug_run  http://localhost:5000/ --
# script_path = ("/").join(os.path.abspath(__file__).split("/")[:-5])
# EB_FILES_DIR = f"{script_path}/TDC_DE/DB"
# DB_JASON = f"{script_path}/TDC_DE/DB_JASON"
# DB_SQL=f"{script_path}/TDC_DE/DB_SQL" # the folder
# def runmode(app):
#     app.run(debug=True)
# ######------------------------------

print("EB_FILES_DIR: ", EB_FILES_DIR)
print("DB_JASON: ", DB_JASON)
print("DB_SQL: ", DB_SQL)

SQLFILE_COPYTO=DB_SQL+"/TDC_DB.db"                            
SQLFILE = os.path.expanduser("~/TDC_DB.db")
print("SQLFILE===>",SQLFILE)
                           


back_2_DB_JASON=("/").join(DB_JASON.split("/")[:-1])
folderpath=back_2_DB_JASON+'/Rep/UCME_BACKUP'
path_out=back_2_DB_JASON+'/Rep/UCME_BACKUP'
SMS_HTML_outmain=path_out+'/USME_sms.html'
SMS_out_groups=path_out+'/GROUPS.html'

abs_path=("/").join(os.path.abspath(__file__).split("/")[:-3])     

update_hour = 9
lastDate_update_path=abs_path+'/Plugins/UPDATE_DATE.log'

TAGS_TYPE = ["*", "RC", "DI", "DO", "AI", "AO",
             "DC", "RPV", "SEQ", "NM", "FL", "ARR", "TM"]
NET = "A"
NET_B = ["930", "800", "690", "650", "651"]
NET_A = ["640", "630", "730", "720", "640", "610", "710", "740", "600"]
PLANT_file_start = {
    "ALL": "??",
    "930": "93",
    "800": "80",
    "690": "69",
    "650": "65",
    "651": "51",
    "640": "64",
    "660": "66",
    "630": "63",
    "730": "73",
    "720": "72",
    "640": "64",
    "610": "61",
    "710": "71",
    "740": "74",
    "600": "60",
}
PLANT_file_rev = {
    "ALL": "??",
    "93": "930",
    "80": "800",
    "69": "690",
    "65": "650",
    "51": "651",
    "64": "640",
    "66": "660",
    "63": "630",
    "73": "730",
    "72": "720",
    "64": "640",
    "61": "610",
    "71": "710",
    "74": "740",
    "60": "600",
}
PLANT_LETTER = {
    "930": "M",
    "800": "j",
    "690": "v",
    "650": "B",
    "651": "U",
    "640": "D",
    "660": "Y",
    "630": "O",
    "634": "W",
    "730": "G",
    "720": "N",
    "620": "N",
    "610": "H",
    "710": "S",
    "740": "R",
    "600": "A",
}
# Define the plant mapping
plant_map = {
    "A": 600,
    "H": 610,
    "B": 700,
    "D": 640,
    "O": 630,
    "W": 634,
    "Q": 630,
    "U": 651,
    "Y": 660,
    "V": 690,
    "S": 710,
    "N": 720,
    "G": 730,
    "R": 740,
    "J": 800,
    "M": 930
}
# ׳›׳� ׳¡׳•׳’ ׳›׳�׳• ׳�׳¢׳¨׳� ׳©׳™׳© ׳�׳• ׳’׳•׳“׳� ׳§׳‘׳•׳¢
lyout_sizes = {
    "NONE": 0,
    "AO": 8,
    "AO_16": 16,
    "HLAI": 16,
    "DI": 32,
    "DO": 16,
    "DO_32": 32,
    "LLMUX": 30,
    "SI": 0
}
# FOR EXPRIAN PVSORC FILES
epks = "//ilnhv-fs01/Shares/WF-OUT/Rep/Experion/*.*"
