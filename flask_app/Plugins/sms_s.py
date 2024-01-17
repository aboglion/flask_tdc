import os,requests,time,json
from flask import render_template

def sms_s(app) :  
  # post שינוי תג ידני מהדף של הטבלה LYOUT
    def is_weekend_or_after_4pm(time_str):
        try:
            # פרקם את המחרוזת לתאריך ושעה
            time_struct = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            
            # בדוק אם התאריך הוא שישי (5) או שבת (6)
            if time_struct.tm_wday == 5 or time_struct.tm_wday == 6:
                return True
            
            # בדוק אם השעה היא אחרי 17:00
            if time_struct.tm_hour >= 17:
                return True
            
            return False
        except ValueError:
            # אם המחרוזת לא בפורמט הנדרש
            return False


    @app.route('/sms_log')
    def sms_log():
            return render_template('sms_logs.html')
    @app.route('/get_sms_log')
    def get_sms_log():
        uri_History = "http://api.multisend.co.il/MultiSendAPI/outboundHistory"
        uri_Today = "http://api.multisend.co.il/MultiSendAPI/outbound"
        # Retrieve the username and password from the configuration   
        api_username = os.getenv('APIUsername')
        api_password = os.getenv('APIPassword')
        # Construct API string
        api_string = [f"{uri_Today}?user={api_username}&password={api_password}&limit=600",\
            f"{uri_History}?user={api_username}&password={api_password}&limit=3000"]
             
        data=[]
    # Make a request to the API
        for api_s in api_string: 
            response = requests.get(api_s)
            try:data.extend(response.json()['outbound_message'])
            except ValueError as e:
                print("Error", "Error parsing response JSON: " + str(e))
                data=[]
                pass
        
        # Process the messages
        html = "<table><tr><th class='timetd' >Time</th><th class='msgtd'>Message</th><th class='idtd'>Id</th></tr>"
        last_id_messages=0
        print(len(data))
        for i in data:
                not_us=False
                if not("ENGR" in i["message"]):not_us=True
                Id=i["message"].split("##")
                if len(Id)>1:Id=Id[1]
                else: continue # ignore the missage that sent form the api directly
                if last_id_messages== Id:continue 
                last_id_messages=Id
                if "password"  in i["message"]: #cript the password that lioned send
                    i["message"]= " \npassword:***** :)\n"+i["message"].split("will")[1]
                if not_us:
                    html += f"<tr class='nono'><td class='timetd'>{i['time']}</td><td class='msgtd'>{i['message']}</td><td class='idtd'>{Id}</td></tr>"
                else:
                    if is_weekend_or_after_4pm(i['time']):
                        html += f"<tr class='no_working'><td class='timetd'>{i['time']}</td><td class='msgtd'>{i['message']}</td><td class='idtd'>{Id}</td></tr>"
                    else:html += f"<tr><td class='timetd'>{i['time']}</td><td class='msgtd'>{i['message']}</td><td class='idtd'>{Id}</td></tr>"
        html += "</table>"

        return html