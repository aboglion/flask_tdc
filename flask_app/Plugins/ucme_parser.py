import re,os
from .sms_parse_helpers import replace_hebrew_with_english,had_a_style,btns,js_end,gr_syle
import TDC_parse_eb.TDC_parse_eb_utils.Consts as Consts


def parse_SMS():
    print("PARSE SMS START NOW :")
    folderpath=Consts.folderpath
    path_out=Consts.path_out
    path = path_out+'/ucme.adb'
    outmain=Consts.SMS_HTML_outmain
    out_groups=Consts.SMS_out_groups


    if not os.path.exists(folderpath) or not os.path.exists(path_out):
        print("the paths not void")
        return False


    try:
        with open(path, 'r', encoding='iso-8859-8') as file:
            lines = file.readlines()  # קורא את כל השורות לרשימה
    except Exception as e: 
        print(e)
        return

    result = []

    for line in lines[1:]:
        # משתמשים ברגולר אקספרשן לפצל לקבוצות בהתאם לרווחים
        groups = re.split(r'\s{2,}', line.strip())
        STATUS="ON"
        TOUT=-2
        TXT=groups[-1]
        NUM=groups[0]
        SEND_TO=""
        try:
            with open(folderpath+"/"+NUM+'.alr', 'r', encoding='iso-8859-8') as file:
                lines = file.readlines()
            if len(lines)>8:
                for line in lines[7:]:
                    if '@SMS' in line or '$' in line  :
                        if line.startswith('$'):
                            line = f'[{line[1:-1]}]'
                        line = line.replace('@SMS', '')

                        SEND_TO+=line+" | "
                    else: break
        except Exception as e: print(e)


                
        if "Permanently" in groups[-2] :
            STATUS="OFF"
            TOUT=-3
        group=groups[TOUT]
        try:int(group)
        except Exception :
            TXT+=group 
            group="00"
        # print(groups[0],groups[1]+groups[2]+groups[3],groups[4],groups[TOUT],STATUS,groups[-1] )
        result.append({"NUM":NUM,"COND":groups[1]+groups[2]+groups[3],"GROUP":groups[4],"TIMEOUT":group,"STATUS":STATUS,"TXT":TXT,"SEND_TO":SEND_TO })
  
    # יצירת דף HTML
    html_code = had_a_style()
    
    

    # הוספת כל קבוצה כרשימה מסודרת בדף HTML    HIDE
    html_code+=btns()
    Table_Hade = '<th>NUM</th><th>COND</th><th>GROUP</th><th>TIMEOUT</th><th>STATUS</th><th>TXT</th><th>SENT TO..</th>'
    Table_Trֹֹֹ_Hade=f"<tr>{Table_Hade}</tr>"
    serchResults='<table><table>'
    html_code+= f'''<div id=serchResults> {serchResults} </div>'''
    html_code += "<table id='cat_tab'>"
    catgoryList=[]

    for item in result:
        if not item["GROUP"]  in catgoryList: catgoryList.append(item["GROUP"])

    for catgory in catgoryList:
        theclass="CLASSֹֹ_"+replace_hebrew_with_english(catgory) 
        html_code +=f'''<tr id={catgory}  onclick="toggleClass('{theclass}')"  > <td colspan="{len(item)}"> <div  class="tag"><h3>︵‿︵‿୨♡°•❀ ⋞{catgory}⋟ ❀•°♡୧‿︵‿︵</h3> </div></td></tr>\n'''       
        html_code +=f'<tr class="hidden-element {theclass}">{Table_Hade}</tr>'
        for item in result:
            if item["GROUP"]==catgory:          
                html_code += f'''<tr {'style="text-decoration: line-through; color: red;"' if item["STATUS"]=="OFF" else 'style=" font-weight: bold;; color:#145A32;"'} id="{item["NUM"]}" class="hidden-element {theclass}"><td>{item["NUM"]}</td><td>{item["COND"]}</td><td>{item["GROUP"]}</td><td>{item["TIMEOUT"]}</td><td>{item["STATUS"]}</td><td>{item["TXT"]}</td><td>{item["SEND_TO"]}</td></tr>'''

            
    html_code += "</table>"

    # סיום דף HTML
    html_code += js_end()

    try:
        # כתיבת קובץ HTML לקובץ
        with open(outmain, 'w+', encoding='utf-8') as file:
            file.write(html_code)
    except Exception as a:
        print(outmain)
        print(a)

    print(f"{outmain} נוצר קובץ ")


    def create_html_table_from_group_files(group_directory=folderpath, output_file=out_groups):
        def reorder_filename(filename):
            reordered_filename=""
            # חלק את התווים לאותיות עבריות ואנגליות
            for char in filename:
                if char==" " or  char=="-" or  char=="_":
                    reordered_filename=" "+reordered_filename+" "
                    continue
                if 'א' <= char and char<= 'ת' and char.isalpha():reordered_filename=char+reordered_filename
                else:reordered_filename=reordered_filename+char  
                        
            return reordered_filename

        # פתח קובץ HTML לכתיבה
        with open(out_groups, 'w', encoding='iso-8859-8') as html_file:
            # התחל את הקובץ ה-HTML
            html_file.write('<html>\n<head>\n<meta charset="iso-8859-8"><title>טבלת קבצי GROUP</title>\n</head>\n')
            html_file.write('<body>\n<table border="1">\n')
            
            html_file.write(
                gr_syle()
            )
            
            # עבור כל קובץ בתיקיית GROUP
            for filename in os.listdir(group_directory):
                # filename=filename.encode('windows-1255').decode('windows-1255')
                print(filename)
                if not filename=='ALL.group' and filename.endswith('.group'):
                    # פתח את הקובץ וקרא את השורות
                    try:
                        with open(group_directory+"/"+filename, 'r',encoding='iso-8859-8') as group_file:
                            file_content = group_file.readlines()
                            filename=".".join(filename.split(".")[:-1])
                            print(filename)
                            html_file.write(f'<th> {filename} </th>\n')
                    except Exception as e:
                        print(e)
                        print(filename)
                        continue
                    # הוסף שורה חדשה לטבלה עם שם הקובץ ותוכנו
                    for line in file_content:
                        # line=line[::-1]
                        try: html_file.write(f'<tr><td >{line.split("@")[0]}</td></tr>\n')
                        except Exception:html_file.write(f'<tr><td >{line}</td></tr>\n')

            # סיים את הטבלה ואת הקובץ ה-HTML
            html_file.write('</table>\n</body>\n</html>\n')

            print('finsh')
    create_html_table_from_group_files(folderpath,out_groups)