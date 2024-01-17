import csv
from datetime import datetime
import random,os
from TDC_parse_eb.TDC_parse_eb_utils.Consts import DB_JASON

csv_file_path = "{DB_JASON}/bar_pvsrc_data.cvs"

def get_color(value, max_value):
    proportion = value / max_value
    red = int(255 * proportion)
    green = int(255 * (1 - proportion))
    return f'rgb({red},{green},0)'

def get_PvsrcBars(current_date,new_value):
    try:
        if os.path.exists(csv_file_path): 
            with open(csv_file_path, "r") as file:
                csv_reader = csv.reader(file)
                data = list(csv_reader)


            
            last_date = data[-1][0] if len(data) > 1 else None

            if last_date != current_date:
                data.append([current_date, new_value])
                if len(data)>31:data=data[-31:]


                with open(csv_file_path, "w", newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(data)
        else:
            data=[]
            data.append([current_date, new_value])
    except Exception as e:
        print(e)
        data = []
        data.append([current_date, new_value])
        pass

    while(len(data)<31):
        data.insert(0,['00.00.00', '0'])


    bars_html = """
     <div class="bar-chart-container">
    """
    dates = [row[0] for row in data]
    vals=[int(row[1]) for row in data]
    max_value = max(vals)
    if not max_value:max_value=1

    for i, (num, date) in enumerate(zip(vals, dates), start=1):
        
        bar_height_vh = (num / max_value) * 20
        bar_color = get_color(num, max_value)
        bar_container_class = "bar-container" if i < len(vals) else "bar-container last-bar"
        bars_html += f"""
        <div class="{bar_container_class}">
        <div class="bar" style="height:{bar_height_vh}vh; background-color: {bar_color};">
            <span class="bar-value">{num}</span>
        </div>
        <div {"hidden" if num==0 else ""} class="bar-label">{date}</div>
         { "<div class='bar-label'>.. יום ריק..יגיע  </div>" if num==0 else ""}
        </div>
        
        """

    bars_html += "</div>"
    


    return bars_html
