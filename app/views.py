#-*-coding:utf-8-*-
from app import app
from flask import render_template,jsonify,request
import HuobiService
import datetime
import time
menus=[
    {"target":"index","name":u"自动炒币","state":"","icon":"icon-edit"},
    {"target":"checkCapital","name":u"炒币查询","state":"","icon":"icon-picture"}
    #{"target":"index","name":"desktop","state":"","icon":"icon-dashboard"}
]


def getMatchresults():
    result={
          "status": "ok",
          "data": [
            {
              "id": 29555,
              "order-id": 59378,
              "match-id": 59335,
              "symbol": "ethusdt",
              "type": "buy-limit",
              "source": "api",
              "price": "100.1000000000",
              "filled-amount": "0.9845000000",
              "filled-fees": "0.0019690000",
              "created-at": 1533200046000
            },
              {
                  "id": 29555,
                  "order-id": 59378,
                  "match-id": 59335,
                  "symbol": "ethusdt",
                  "type": "sell-limit",
                  "source": "api",
                  "price": "101.1000000000",
                  "filled-amount": "0.9845000000",
                  "filled-fees": "0.0019690000",
                  "created-at": 1533100046000
              }

          ]
        }
    return result
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
    #print menus
    return render_template("/used/index.html",menus=menus)

@app.route("/api/kline",methods=['GET', 'POST'])
def getKline():
    symbol=request.args.get("symbol")
    period=request.args.get("period")
    size=request.args.get("size",type=int,default=150)
    #print symbol,period,size
    infos=HuobiService.get_kline(symbol, period, size)
    #print infos
    klines=[]
    times=[]
    buyLimit=[]
    sellLimit=[]
    curTime=datetime.datetime.now()
    #print curTime
    for item in infos["data"]:
        tmp=[]
        tmp.append(item["open"])
        tmp.append(item["close"])
        tmp.append(item["low"])
        tmp.append(item["high"])
        buyLimit.append(0)
        sellLimit.append(0)
        klines.append(tmp)
        #times.append(time.strftime("%d %M"),curTime)
        times.append(curTime.strftime("%m-%d %H"))
        if period=="30min":
            curTime-=datetime.timedelta(minutes=1)
        elif period=="60min":
            curTime-=datetime.timedelta(hours=1)
        elif period=="1day":
            curTime-=datetime.timedelta(days=1)


    #print times
    klines.reverse()
    times.reverse()

    matchresults=getMatchresults()
    matchRecords=[]

    for item in matchresults["data"]:
        #print item["created-at"]
        timeTmp=time.strftime("%m-%d %H",time.localtime(item["created-at"]/1000))
        index=times.index(timeTmp)
        #print index
        if item["type"]=="buy-limit":
            buyLimit[index]=item["filled-amount"]
        elif item["type"]=="sell-limit":
            sellLimit[index]=item["filled-amount"]


        tmpItem=[]
        tmpItem.append(item["type"])
        tmpItem.append(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(item["created-at"]/1000)))
        tmpItem.append(item["filled-amount"])
        tmpItem.append(item["filled-fees"])
        tmpItem.append(item["price"])


        matchRecords.append(tmpItem)

    return jsonify({"klines":klines,
                    "times":times,
                    "buy-limit":buyLimit,
                    "sell-limit":sellLimit,
                    "matchRecords":matchRecords})

@app.route("/api/getBalance",methods=['GET', 'POST'])
def getBalance():
    balances=HuobiService.get_balance()
    #print balances
    tradeBalance=0
    frozenBalance=0
    #print balances
    for item in  balances["data"]["list"]:
        if item["currency"]=="usdt" and item["type"]=="trade":
            tradeBalance=item["balance"]
        if item["currency"] == "usdt" and item["type"] == "frozen":
            frozenBalance = item["balance"]
    return jsonify({"tradeBalance":tradeBalance,"frozenBalance":frozenBalance})
@app.route('/checkCapital', methods=['GET', 'POST'])
def checkCapital():

    #return render_template("index.html")
    fillMenus(menus,1)
    #print menus
    return render_template("/used/check.html",menus=menus)



