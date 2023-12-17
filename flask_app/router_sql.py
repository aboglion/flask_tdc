from flask import Flask, render_template, request, redirect
from tinydb import TinyDB, Query
import time,os,Plugins

from TDC_parse_eb.TDC_parse_eb_utils.Consts import DB_SQL,EB_FILES_DIR,plant_map,PLANT_file_rev
from TDC_parse_eb.TDC_parse_eb_utils.hebrew import fix_if_reversed
import sqlite3,os,glob
import threading
from concurrent.futures import ThreadPoolExecutor
xx_path=EB_FILES_DIR[:-2]+"Rep/*.XX"
print("xx_path:",xx_path)
XX_FILES=glob.glob(xx_path)
print("XX_FILES:",XX_FILES)



if not os.path.exists(DB_SQL):
    os.makedirs(DB_SQL)

 
 

def router_SQL(app):

    def run_query(DB_file, query):
        try:
            conn = sqlite3.connect(DB_file)
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            if rows:
                # Get column names
                column_names = [description[0] for description in cursor.description]

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
                return html_table

            else:
                conn.close()
                return "<h1>No data found.</h1>"

        except sqlite3.Error as e:
            conn.close()
            return f"<h1>An error occurred: {e}</h1>"


            
    table_names='''
                SELECT name FROM sqlite_master WHERE type='table';
                '''
    ALLDB_A_50='SELECT * FROM ALLDB_A LIMIT 50;'

    from urllib.parse import unquote

    @app.route("/q_test/")
    @app.route("/q_test/<Q>")
    def q_test(Q=table_names):
        Q=unquote(Q) 
        print(Q)
        # Saving the output to an HTML file
        # output_file = "table_names.html"
        # with open(output_file, 'w') as file:
        #     file.write(run_query("TDC.db",table_names))

        # # Saving the output to an HTML file
        # output_file = "ALLDB_A_50.html"
        # with open(output_file, 'w') as file:
        #     file.write(run_query("TDC.db",ALLDB_A_50))
        res_html = run_query("TDC.db",Q)
        return render_template('QUERY.html', res_html=res_html,Q=Q)




def SAVE_sqlite(data, names, DB_file, Table):
    conn = None
    try:
        conn = sqlite3.connect(DB_file)
        cursor = conn.cursor()

        # Create table with dynamic columns
        CREATE_TABLE_txt = f"CREATE TABLE IF NOT EXISTS {Table} ("
        for n in names:
            CREATE_TABLE_txt += f'''"{n}" {'INTEGER' if 'NUM' in n else 'TEXT'},'''
        CREATE_TABLE_txt = CREATE_TABLE_txt.rstrip(',') + ', "UPDATING_DATA" TEXT)'
        cursor.execute(CREATE_TABLE_txt)
        
        # Insert data with dynamic placeholders
        placeholders = ', '.join(['?'] * len(names) + ['?'])  # one extra for UPDATING_DATA
        INSERT_txt = f'INSERT INTO {Table} VALUES ({placeholders})'
        
        for line in data:
            if len(line) != len(names) + 1:  # +1 for UPDATING_DATA
                print(f"Data length mismatch in table {len(line)}: {len(names) + 1}")
                print(names)
                print(line)
                print("------------")
                continue  # Skip this row or handle as needed
            cursor.execute(INSERT_txt, line)
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        if conn:
            conn.close()
        print("Finish SQL")



def xxToSql(mode=False):


    def process_file(file_path,DB_file,table_name):
        
        updated=False
        names,data =[],[]
        Columns=0
        print(f"Processing file => : {file_path}")
        TABLE_EXISTS = False 
        try:
            with open(file_path, 'r', encoding='windows-1255') as file:              
                updated="-----"
                dicrption_index=0
                for index,line in enumerate(file):
                    if "Data type changed" in line or 'ERRORS DETECTE' in line or "Request failed" in line:
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
                        dicrption_index=parts.index("PTDESC")
                        Columns=len(parts)
                        continue
                    if index==2 and not(parts[0] == "ENTITY"):
                        raise Exception(f"Invalid FILE \n , the file must have titles in thered line (({index}))  <<<<<<<<<<<|\n")


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
            SAVE_sqlite(data,names,DB_file,table_name)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
        finally:
            print(f"Finished processing =|: {file_path}")

    def main_xxsql(update):
        global DB_SQL
        # for file_path in XX_FILES:
        #     table_name = os.path.basename(file_path).split('.')[0]
        #     process_file(file_path,DB_SQL+"/TDC99.db",table_name) 
        if update:
            print("main_xxsql start")
            with ThreadPoolExecutor(max_workers=4) as executor:
                try:
                    DB_SQL = DB_SQL + "/TDC.db"
                    for file_path in XX_FILES:
                        table_name = os.path.basename(file_path).split('.')[0]
                        executor.submit(process_file, file_path,DB_SQL,table_name)

                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    print(f"Error: {e}")
        print("main_xxsql=false")
    main_xxsql(mode)






