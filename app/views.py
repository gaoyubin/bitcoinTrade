#-*-coding:utf-8-*-
from app import app
from flask import render_template,jsonify,request
import HuobiService
from helpler import ts_to_time

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
    symbol=request.args.get("symbol", default="btcusdt")
    period=request.args.get("period", default="1min")
    size=request.args.get("size",type=int,default=300)
    ret = {}
    data_pre = HuobiService.get_kline(symbol,period,size)
    kline = []
    for item in data_pre["data"]:
        temp = []
        time = ts_to_time(item['id'])
        temp.append(time)
        temp.append(item['open'])
        temp.append(item['close'])
        temp.append(item['low'])
        temp.append(item['high'])
        kline.append(temp)
    ret['data'] = kline
    return jsonify(ret)


@app.route('/checkCapital', methods=['GET', 'POST'])
def checkCapital():

    #return render_template("index.html")
    fillMenus(menus,1)
    print menus
    return render_template("/used/check.html",menus=menus)



