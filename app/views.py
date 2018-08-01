#-*-coding:utf-8-*-
from app import app
from flask import render_template,jsonify,request
import HuobiService

menus=[
    {"target":"index","name":u"自动炒币","state":"","icon":"icon-edit"},
    {"target":"checkCapital","name":u"炒币查询","state":"","icon":"icon-picture"}
    #{"target":"index","name":"desktop","state":"","icon":"icon-dashboard"}
]

def fillMenus(menus,index):
    for i in range(len(menus)):
        if i==index:
            menus[i]["state"]="active"
        else:
            menus[i]["state"]=""


@app.route('/',methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    #return render_template("index.html")
    fillMenus(menus,0)
    print menus
    return render_template("/used/index.html",menus=menus)

@app.route("/api/kline",methods=['GET', 'POST'])
def getKline():
    symbol=request.args.get("symbol")
    period=request.args.get("period")
    size=request.args.get("size",type=int,default=150)
    return jsonify(HuobiService.get_kline(symbol,period,size))


@app.route('/checkCapital', methods=['GET', 'POST'])
def checkCapital():

    #return render_template("index.html")
    fillMenus(menus,1)
    print menus
    return render_template("/used/check.html",menus=menus)



