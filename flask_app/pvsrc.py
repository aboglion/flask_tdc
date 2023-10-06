from flask import Flask, render_template, request, redirect
from tinydb import TinyDB, Query
import time,os,Plugins
from TDC_parse_eb.TDC_parse_eb_utils.Consts import DB_JASON
from TDC_parse_eb.TDC_parse_eb_utils.hebrew import fix_if_reversed

if not os.path.exists(DB_JASON):
    os.makedirs(DB_JASON)

def router_pvsrc(app):
    today_ = time.strftime("%d-%b-%Y", time.gmtime())

    @app.route("/pvsrc")
    def pvsrc():
        data=Plugins.Get_DBJson_Data('PVSRC_TODAY_DB.json')
        return render_template("pvsrc_main.html", data=data)

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
