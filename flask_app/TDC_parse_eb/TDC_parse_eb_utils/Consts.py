
import os
defult_STATUS = "existed"

### ---------runmode togals--------

### compose  http://localhost
EB_FILES_DIR="/TDC/DB"
DB_JASON="/TDC/DB_JASON"
def runmode(app):
    print("SERVER RUNING")

# ## debug_run  http://localhost:5000/
# script_path = ("/").join(os.path.abspath(__file__).split("/")[:-5])
# EB_FILES_DIR = f"{script_path}/TDC_debug/DB"
# DB_JASON = f"{script_path}/TDC_debug/DB_JASON"
# def runmode(app):
#     app.run(debug=True)

# -------------------------------y


update_hour = 9

TAGS_TYBE = ["*", "RC", "DI", "DO", "AI", "AO",
             "DC", "RPV", "SEQ", "NM", "FL", "ARR", "TM"]
NET = "A"
NET_B = ["320", "800", "690", "650", "651"]
NET_A = ["640", "630", "730", "720", "640", "610", "710", "740", "600"]
PLANT_file_start = {
    "ALL": "??",
    "320": "32",
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
PLANT_LETTER = {
    "320": "M",
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
    "640": "N",
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
    "M": 320
}
# כל סוג כמו מערך שיש לו גודל קבוע
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
