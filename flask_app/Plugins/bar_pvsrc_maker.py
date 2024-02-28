import csv
from datetime import datetime
import random, os
from TDC_parse_eb.TDC_parse_eb_utils.Consts import DB_JASON

# Corrected the file extension here
csv_file_path = f"{DB_JASON}/bar_pvsrc_data.csv"

def get_color(value, max_value):
    proportion = value / max_value
    red = int(255 * proportion)
    green = int(255 * (1 - proportion))
    return f'rgb({red},{green},0)'

def get_PvsrcBars(current_date, new_value):
    try:
        print(csv_file_path, "\n\n")
        with open(csv_file_path, "r") as file:
            csv_reader = csv.reader(file)
            data = sorted(list(csv_reader), key=lambda x: datetime.strptime(x[0], '%d.%m.%y'))
            print(data[-1][0])
        last_date = data[-1][0] if len(data) > 1 else None

        if last_date != str(current_date):
            data.append([current_date, new_value])
            # Sort again after appending the new entry to ensure correct order
            data = sorted(data, key=lambda x: datetime.strptime(x[0], '%d.%m.%y'))
            if len(data) > 31:
                # Ensure we keep the most recent 31 records
                data = data[-31:]
            with open(csv_file_path, "w", newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(data)

    except Exception as e:
        print(e)
        data = []
        data.append([current_date, new_value])


    while(len(data) < 31):
        data.insert(0, ['00.00.00', '0'])
    print(data)
    bars_html = """
     <div class="bar-chart-container">
    """
    dates = [row[0] for row in data]
    vals = [int(row[1]) for row in data]
    max_value = max(vals) if vals else 1

    for i, (num, date) in enumerate(zip(vals, dates), start=1):
        
        bar_height_vh = (num / max_value) * 20 if max_value else 0
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
