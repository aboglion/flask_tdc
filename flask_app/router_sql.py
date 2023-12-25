from flask import Flask, render_template, request, redirect,Response
from tinydb import TinyDB, Query
import time,os,Plugins,shutil,chardet

from TDC_parse_eb.TDC_parse_eb_utils.Consts import DB_SQL,EB_FILES_DIR,plant_map,PLANT_file_rev,SQLFILE,SQLFILE_COPYTO
from TDC_parse_eb.TDC_parse_eb_utils.hebrew import fix_if_reversed
import sqlite3,os,glob
import threading
from concurrent.futures import ThreadPoolExecutor
import threading
xx_path=EB_FILES_DIR[:-2]+"Rep/*.XX"
print("xx_path:",xx_path)
XX_FILES=glob.glob(xx_path)
print("XX_FILES:",XX_FILES)

db_lock = threading.Lock()


if not os.path.exists(DB_SQL):
    os.makedirs(DB_SQL)

def GET_file_encoding(file):
    with open(file, 'rb') as f:
        result = chardet.detect(f.read())
        encoding_ = result['encoding']
        if encoding_ == "utf-8":
            return encoding_
	else:return "windows-1255"

def copy_file(local=SQLFILE, out=SQLFILE_COPYTO):
    if not os.path.exists(local) and os.path.exists(out):
        try:
            shutil.copy(out, local)
        except Exception as e:
            print(f"SQL Error local out to local: {e}")
    elif os.path.exists(local):
        try:
            shutil.copy(local, out)
        except Exception as e:
            print(f"SQL Error local copy to out : {e}")
 

def router_SQL(app):

    def run_query(query):
        global SQLFILE
        try:
            SAVED_Q=False
            conn = sqlite3.connect(SQLFILE)
            print(SQLFILE,"=<+++++++++++=")
            if "SELECT" in query:
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                th= cursor.description
                conn.close()
            else:rows=False
            conn = sqlite3.connect(SQLFILE)
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS SAVED_Q ("NAMED"  TEXT PRIMARY KEY, "VAL" TEXT)')
            conn.close()
            conn = sqlite3.connect(SQLFILE)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM SAVED_Q LIMIT 100;')
            SAVED_Q = cursor.fetchall()
            conn.close()

            if rows:
                # Get column names
                column_names = [description[0] for description in th]

                # Start HTML structure with CSS
                html_table = """ 
                <table>
                <tr>""" + "".join(f"<th>{name}</th>" for name in column_names) + "</tr>"
                
                # Add data rows
                for row in rows:
                    html_table += "<tr>" + "".join(f"<td>{value}</td>" for value in row) + "</tr>"
                
                html_table += """
                </table>
                """
                conn.close()
                return [html_table,SAVED_Q]

            else:
                if conn:
                    conn.close()
                if rows==False:return ["<h1>קלט לא חוקי</h1>",SAVED_Q]
                return ["<h1>No data found.</h1>",SAVED_Q]

        except sqlite3.Error as e:
            conn.close()
            return [f"<h1>An error occurred: {e}</h1>",SAVED_Q]


    table_names='''
                SELECT * FROM sqlite_master WHERE type='table';
                '''
    ALLDB_A_50='SELECT * FROM ALLDB_A LIMIT 50;'

    from urllib.parse import unquote

    @app.route("/q_test/")
    @app.route("/q_test/<Q>")
    def q_test(Q=table_names):
        global SQLFILE
        if not os.path.exists(SQLFILE):copy_file()
        Q=unquote(Q) 
        # print(Q)
        RES = run_query(Q)
        res_html=RES[0]
        SAVED_Q=RES[1]

        return render_template('QUERY.html', res_html=res_html,Q=Q,SAVED_Q=SAVED_Q)



    @app.route("/q_save/<name>/<query>")
    def q_save(name,query):
            try:
                conn = sqlite3.connect(SQLFILE)
                cursor = conn.cursor()
                print(name)
                CREATE_TABLE_txt = f'CREATE TABLE IF NOT EXISTS SAVED_Q ("NAMED" "TEXT", "VAL" "TEXT")'
                cursor.execute(CREATE_TABLE_txt)
                cursor.execute('INSERT OR REPLACE INTO SAVED_Q ("NAMED", "VAL") VALUES (?, ?)', (str(name), str(query)))
                conn.commit()
                conn.close()
                return q_test(query)
            except sqlite3.Error as e:
                conn.commit()
                conn.close()
                copy_file()
                return(f"SQLite error: {e}")

    @app.route("/q_delete/<name>")
    def q_delete(name):
        try:
            conn = sqlite3.connect(SQLFILE)
            cursor = conn.cursor()
            
            # SQL query to delete the entry with the given name
            cursor.execute('DELETE FROM SAVED_Q WHERE NAMED = ?', (name,))

            # Commit the changes and close the connection
            conn.commit()
            conn.close()
            copy_file()
            return q_test('SELECT * FROM SAVED_Q LIMIT 100;')

        except sqlite3.Error as e:
            conn.close()
            return f"SQLite error: {e}"
    @app.route('/sql/', methods=['POST', 'GET'])
    def sq():
            xxToSql(1)
            return redirect("/q_test")
    
def SAVE_sqlite(data, names, SQLFILE, Table):
    conn = None
    try:
        conn = sqlite3.connect(SQLFILE)
        cursor = conn.cursor()

        print("Finish SQL")
        # Create table with dynamic columns
        CREATE_TABLE_txt = f'CREATE TABLE IF NOT EXISTS {Table} ("{names[0].strip()}" TEXT PRIMARY KEY,'
        for n in names[1:]:
            CREATE_TABLE_txt += f'''"{n}" {'INTEGER' if 'NUM' in n else 'TEXT'},'''
        CREATE_TABLE_txt = CREATE_TABLE_txt.rstrip(',') + ', "UPDATING_DATA" TEXT)'
        print(CREATE_TABLE_txt)
        cursor.execute(CREATE_TABLE_txt)
        
        # Insert data with dynamic placeholders
        placeholders = ', '.join(['?'] * len(names) + ['?'])  # one extra for UPDATING_DATA
        INSERT_txt = f'INSERT OR REPLACE INTO {Table} VALUES ({placeholders})'
        
        for line in data:
            if len(line) != len(names) + 1:  # +1 for UPDATING_DATA
                print(f"Data length mismatch in table {len(line)}: {len(names) + 1}")
                print(names)
                print(line)
                print("------------")
                continue  # Skip this row or handle as needed
        
            cursor.execute(INSERT_txt, line)
        
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        conn.close()
        print(f"SQLite error: {e}")
    finally:
        if conn:
            conn.close()
        print("Finish SQL")



def xxToSql(mode=0):
    print(mode,"<<----------")

    def process_file(file_path,SQLFILE,table_name):
        
        updated,NO_PTDESC=False,False
        names,data =[],[]
        Columns,CMPLTIME_index=0,0
        print(f"Processing file => : {file_path}")
        TABLE_EXISTS = False 
        try:
            with open(file_path, 'r', encoding=GET_file_encoding(file_path)) as file:              
                updated="-----"
                dicrption_index=0
                for index,line in enumerate(file):
                    if "Data type changed" in line or 'ERRORS DETECTE' in line or "Request failed" in line or "NO MATCH FOUND" in line:
                        continue
                    # print(index,line)
                    if index==0 and "QUERY DESCRIPTOR:" in line:
                        parts = line.split(">")
                        if len(parts) > 1:
                            updated = "# FILE:" + parts[-1].strip() + "  # "
                        continue
                    if index==0 and not ("QUERY DESCRIPTOR:" in line):
                        raise Exception(f"Invalid FILE ,\n The file does not contain a valid first line ({index}) with the file name  <<<<<<<<<<<|\n")
                
                    if index==1 and "INVOCATION TIME:" in line:
                        parts = line.split(":")
                        if len(parts) > 3:
                            updated += "TIME:" + ":".join(parts[1:3]).strip()
                        continue
                    if index==1 and not("INVOCATION TIME:" in line):
                        raise Exception(f"Invalid FILE ,\n The file does not contain a valid second line ({index}) with the query description  <<<<<<<<<<<|\n")


                    parts = line.strip().split()

                    if index==2 and parts[0] == "ENTITY":
                        names = [p.replace('(', '_').replace(')', '') for p in parts]
                        if "PTDESC" in parts:dicrption_index=parts.index("PTDESC")
                        else:NO_PTDESC=True
                        if "CMPLTIME" in parts: #fix date '05/23/21 07:36:03' to be one
                            CMPLTIME_index=parts.index("CMPLTIME")
                        Columns=len(parts)
                        continue
                    if index==2 and not(parts[0] == "ENTITY"):
                        raise Exception(f"Invalid FILE \n , the file must have titles in thered line (({index}))  <<<<<<<<<<<|\n")

                    #fix date '05/23/21 07:36:03' to be one
                    if CMPLTIME_index and not parts[CMPLTIME_index]=="0-00:00:00":
                        parts[CMPLTIME_index]=parts[CMPLTIME_index]+" "+parts[CMPLTIME_index+1]
                        parts.remove(parts[CMPLTIME_index + 1])
                        Columns=len(parts)-1


                    
                    # add pant name
                    if "PLANT" not in names:names.append("PLANT")
                    if parts[0][:2].isdigit() and str(parts[0][:2]) in PLANT_file_rev:
                        parts.append(str(PLANT_file_rev[str(parts[0][:2])]))
                    elif str(parts[0][0]) in plant_map:
                        parts.append(str(plant_map[str(parts[0][0])]))
                    else: parts.append("00")
                    # Columns=Columns+1
                    # print(Columns,parts)
                    # exit()

                    if not NO_PTDESC:
                    #>תיקון התיאור
                        if len(parts) > Columns:
                            part2=(Columns-(dicrption_index))

                            # if dicrption at the end 
                            if part2==0:
                                dicrption = " ".join(parts[dicrption_index:])
                                parts = parts[:dicrption_index]
                                parts.insert(dicrption_index,fix_if_reversed(dicrption))

                            # if dicrption in the middle 
                            else:
                                dicrption = " ".join(parts[dicrption_index:-part2])
                                parts = parts[:dicrption_index] + parts[-part2:]
                                parts.insert(dicrption_index,fix_if_reversed(dicrption))

                            #if dicrption is empty
                        if len(parts) <= Columns:parts.insert(dicrption_index,"----")


                    parts.append(updated)
                    data.append(parts)
            SAVE_sqlite(data,names,SQLFILE,table_name)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
        finally:
            print(f"Finished processing =|: {file_path}")

    def main_xxsql(modexx):
        global DB_SQL,XX_FILES,SQLFILE
        if modexx==1:
            try:
                for file_path in XX_FILES:
                    table_name = os.path.basename(file_path).split('.')[0]
                    process_file(file_path,SQLFILE,table_name) 
                print("main_xxsql start")
                # with ThreadPoolExecutor(max_workers=4) as executor:
                
                #     DB_SQL = DB_SQL + "/TDC.db"
                #     for file_path in XX_FILES:
                #         table_name = os.path.basename(file_path).split('.')[0]
                #         executor.submit(process_file, file_path,DB_SQL,table_name)
                copy_file()
            except Exception as e:
                    import traceback
                    traceback.print_exc()
                    print(f"Error: {e}")
        print("main_xxsql=false",modexx)
    main_xxsql(mode)






