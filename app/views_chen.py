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

@app.route("/api/balance")
def getBalance():
    '''
        /* GET /v1/account/accounts/'account-id'/balance */
        {
          "status": "ok",
          "data": {
            "id": 100009,
            "type": "spot",
            "state": "working",
            "list": [
              {
                "currency": "usdt",
                "type": "trade",
                "balance": "500009195917.4362872650"
              },
              {
                "currency": "usdt",
                "type": "frozen",
                "balance": "328048.1199920000"
              },
             {
                "currency": "etc",
                "type": "trade",
                "balance": "499999894616.1302471000"
              },
              {
                "currency": "etc",
                "type": "frozen",
                "balance": "9786.6783000000"
              }
             {
                "currency": "eth",
                "type": "trade",
                "balance": "499999894616.1302471000"
              },
              {
                "currency": "eth",
                "type": "frozen",
                "balance": "9786.6783000000"
              }
            ],
            "user-id": 1000
          }
        }
    '''

    # 现在暂时用假数据代替
    import random

    ret = dict()
    ret['status'] = 'OK'
    ret['list'] = []
    ret['list'].append({
                "currency": "usdt",
                "type": "trade",
                "balance": "{}".format(random.randrange(90, 110))})

    return jsonify(ret)

@app.route('/api/history')
def get_history(symbol='btcusdt', size=10):
    '''
    获取交易记录
    :return:
    '''
    data = []
    import random
    for i in range(size):
        temp = [];
        #amount  price direction time
        temp.append(random.random())
        temp.append( random.randrange(500, 600))
        temp.append("buy")
        temp.append("2019.10.1")
        data.append(temp)
    return jsonify(data)


@app.route('/checkCapital', methods=['GET', 'POST'])
def checkCapital():

    #return render_template("index.html")
    fillMenus(menus,1)
    print menus
    return render_template("/used/check.html",menus=menus)



