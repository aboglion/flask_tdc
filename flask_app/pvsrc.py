from flask import Flask, render_template, request, redirect
from markupsafe import Markup
from tinydb import TinyDB, Query
import time,os,Plugins
from TDC_parse_eb.TDC_parse_eb_utils.Consts import DB_JASON
from TDC_parse_eb.TDC_parse_eb_utils.hebrew import fix_if_reversed
from TDC_parse_eb.pvsrc_parser import extract_date_from_file

if not os.path.exists(DB_JASON):
    os.makedirs(DB_JASON)


def router_pvsrc(app):
    today_ = time.strftime("%d-%b-%Y", time.gmtime())



    @app.route("/pvsrc")
    def pvsrc():

        updated_date=Plugins.Get_Last_UpdateDate()
        actionUpdateData=Plugins.Update_Data()
        if actionUpdateData:return redirect(actionUpdateData)

        #CHECK AND UPDATE OR WAIT UNTIL UPDATE FINSH
        data=Plugins.Get_DBJson_Data('PVSRC_TODAY_DB.json')
        for d in data :print(d['ENTITY'])
        sorted_data = sorted(data, key=lambda item: item['ENTITY'][:3])
        data_len=len(sorted_data)
        files_update_date=extract_date_from_file()
        bars_DIV=Markup(Plugins.get_PvsrcBars(files_update_date if files_update_date else today_,data_len))
        return render_template("pvsrc_main.html", data=sorted_data,bars_DIV=bars_DIV)

    @app.route("/save", methods=["POST"])
    def save_reason():
        db = TinyDB(DB_JASON+'/PVSRC_TODAY_DB.json')
        witch = request.form.get("witch")
        value = request.form.get("value")
        db.update({"REASON": value}, Query()["ENTITY"] == witch)
        PVSRC_HISTORY_DB = TinyDB(DB_JASON+'/PVSRC_HISTORY_DB.json')
        e = db.search(Query()["ENTITY"] == witch)
        e[0].update({"END_AT": "updated:"+today_})
        e[0].pop("NEW", None)
        a = PVSRC_HISTORY_DB.insert(dict(e[0]))
        db.close()
        return redirect(f"/pvsrc#{witch}")

    @app.route("/history/<entity>")
    def history(entity):
        Entity = Query()
        hi = TinyDB(DB_JASON + "/PVSRC_HISTORY_DB.json")
        data = hi.search(Entity["ENTITY"] == entity)
        hi.close()
        if len(data) == 0:
            return render_template("pvsrc_hist_404.html", data=entity)
        return render_template("pvsrc_history.html", data=data)

    @app.route('/back')
    def back():
        return redirect("/pvsrc")
