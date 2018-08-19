#-*-coding:utf-8-*-
from app import app
from flask import render_template, jsonify, request
from . import HuobiService

from helpler import ts_to_time
from subprocess import Popen
from app import trade_proc

import datetime
import time

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.contrib.timeseries.python.timeseries import NumpyReader

menus = [
    {
        "target": "index",
        "name": "自动炒币",
        "state": "",
        "icon": "icon-edit"
    }, {
        "target": "checkCapital",
        "name": "炒币查询",
        "state": "",
        "icon": "icon-picture"
    }
    #{"target":"index","name":"desktop","state":"","icon":"icon-dashboard"}
]


def getMatchresults():
    result = {
        "status":
        "ok",
        "data": [{
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
        }, {
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
        }]
    }

    return result


def fillMenus(menus, index):
    for i in range(len(menus)):
        if i == index:
            menus[i]["state"] = "active"
        else:
            menus[i]["state"] = ""


#@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    #return render_template("index.html")
    fillMenus(menus, 0)
    #print menus

    return render_template("/index.html", menus=menus)


@app.route("/api/kline", methods=['GET', 'POST'])
def getKline():
    symbol = request.args.get("symbol", default="btcusdt")
    period = request.args.get("period", default="1min")
    size = request.args.get("size", type=int, default=300)
    ret = {}
    data_pre = HuobiService.get_kline(symbol, period, size)
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

import urllib.request
import re
import json
def getUSDCNY():
    fp = urllib.request.urlopen(
        'http://webforex.hermes.hexun.com/forex/quotelist?code=FOREXUSDCNY,&column=code,price,UpdownRate&callback=ongetjsonpforex&_=1451543515359')
    html = fp.read().decode("utf-8")
    fp.close()
    s = re.findall("\((.*)\)", str(html))[0]
    sjson = json.loads(s)
    USDCNY = sjson["Data"][0][0][1] / 10000.0
    return USDCNY
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
        "balance": "{}".format(random.randrange(90, 110))
    })

    symbol="btcusdt"
    info=HuobiService.get_trade(symbol)
    price=info["tick"]["data"][0]["price"]
    balances = HuobiService.get_balance()
    total=0
    for item in balances["data"]["list"]:
        if(item["currency"]=="usdt"):
            total+=float(item["balance"])
        elif(item["currency"]=="btc"):
            total+=float(item["balance"])*float(price)

    print (total)
    #print (balances)
    print (getUSDCNY())
    total=total*getUSDCNY()*1.00732
    #print (total*getUSDCNY())
    return jsonify({"total":total})

en2chOfType={"buy-market":"市价买","sell-market":"市价卖","buy-limit":"限价买",
"sell-limit":"限价卖"
             }
@app.route('/api/history')
def get_history(symbol='btcusdt', size=10):
    '''
    获取交易记录
    :return:
    '''

    data = []

    '''
    import random
    
    for i in range(size):
        temp = []
        # amount price direction time
        temp.append("2019.10.1")
        temp.append("买入")
        temp.append(random.randrange(5000, 6000))
        temp.append(random.random())
        data.append(temp)

    '''
    symbol="btcusdt"
    matchresults=HuobiService.orders_matchresults(symbol)
    matchRecords=[]
    for item in matchresults["data"]:
        #print item["created-at"]




        tmpItem = []
        tmpItem.append(
            time.strftime("%Y-%m-%d %H:%M:%S",
                          time.localtime(item["created-at"] / 1000)))



        tmpItem.append(en2chOfType[item["type"]])
        tmpItem.append('{:.2f}'.format(float(item["price"])))
        tmpItem.append('{:.1f}'.format(float(item["filled-amount"])*10000));
        #tmpItem.append(item["filled-fees"])


        matchRecords.append(tmpItem)
    print (matchRecords)
    return jsonify(matchRecords)


@app.route('/api/start')
def start_trade():
    '''
    开始交易
    :return:
    '''
    global trade_proc
    args = ['python', 'worker.py']

    if trade_proc == 1440:
        trade_proc = Popen(args)
    elif not trade_proc.poll():  # 交易进程还没结束
        return jsonify({'msg': "It's been running!"})
    else:
        trade_proc = Popen(args)

    return jsonify({'msg': 'start success!'})


@app.route('/api/stop')
def stop_trade():
    '''
    停止交易
    :return:
    '''
    global trade_proc

    if trade_proc and trade_proc != 1440:
        trade_proc.terminate()

    return jsonify({'msg': 'Stop success!'})


@app.route('/api/runstate')
def get_trade_state():
    if trade_proc == 1440 or trade_proc.poll():
        return jsonify({"status": "stop"})
    else:
        return jsonify({"status": "running"})


@app.route("/api/check/getkline", methods=['GET', 'POST'])
def checkGetKline():
    symbol = request.args.get("symbol")
    period = request.args.get("period")
    size = request.args.get("size", type=int, default=150)
    #print symbol,period,size
    infos = HuobiService.get_kline(symbol, period, size)
    #print infos
    klines = []
    times = []
    buyLimit = []
    sellLimit = []
    curTime = datetime.datetime.now()
    #print curTime

    for item in infos["data"]:
        tmp = []
        tmp.append(item["open"])
        tmp.append(item["close"])
        tmp.append(item["low"])
        tmp.append(item["high"])
        buyLimit.append(0)
        sellLimit.append(0)
        klines.append(tmp)
        #times.append(time.strftime("%d %M"),curTime)
        times.append(curTime.strftime("%m-%d %H"))

        if period == "30min":
            curTime -= datetime.timedelta(minutes=1)
        elif period == "60min":
            curTime -= datetime.timedelta(hours=1)
        elif period == "1day":
            curTime -= datetime.timedelta(days=1)

    #print times
    klines.reverse()
    times.reverse()

    matchresults = getMatchresults()
    matchRecords = []

    for item in matchresults["data"]:
        #print item["created-at"]
        timeTmp = time.strftime("%m-%d %H",
                                time.localtime(item["created-at"] / 1000))
        index = times.index(timeTmp)
        #print index

        if item["type"] == "buy-limit":
            buyLimit[index] = item["filled-amount"]
        elif item["type"] == "sell-limit":
            sellLimit[index] = item["filled-amount"]

        tmpItem = []
        tmpItem.append(item["type"])
        tmpItem.append(
            time.strftime("%Y-%m-%d %H:%M:%S",
                          time.localtime(item["created-at"] / 1000)))
        tmpItem.append(item["filled-amount"])
        tmpItem.append(item["filled-fees"])
        tmpItem.append(item["price"])

        matchRecords.append(tmpItem)

    return jsonify({
        "klines": klines,
        "times": times,
        "buy-limit": buyLimit,
        "sell-limit": sellLimit,
        "matchRecords": matchRecords
    })


@app.route("/api/check/getBalance", methods=['GET', 'POST'])
def checkGetBalance():
    balances = HuobiService.get_balance()
    #print balances
    tradeBalance = 0
    frozenBalance = 0
    #print balances

    for item in balances["data"]["list"]:
        if item["currency"] == "usdt" and item["type"] == "trade":
            tradeBalance = item["balance"]

        if item["currency"] == "usdt" and item["type"] == "frozen":
            frozenBalance = item["balance"]

    return jsonify({
        "tradeBalance": tradeBalance,
        "frozenBalance": frozenBalance
    })


@app.route('/checkCapital', methods=['GET', 'POST'])
def checkCapital():

    #return render_template("index.html")
    fillMenus(menus, 1)
    #print menus

    return render_template("/check.html", menus=menus)

@app.route('/', methods=['GET'])
@app.route('/homePage', methods=['GET'])
def homePage():

    #return render_template("homePage.html")
    fillMenus(menus, 1)
    #print menus

    return render_template("/homePage.html")

@app.route('/api/predict', methods=['GET'])
def predict():
    kline_data = HuobiService.get_kline('btcusdt', '1min', 2000)
    kline = pd.DataFrame(kline_data['data'])
    closed = kline['close']
    closed = closed.values[::-1]
    ts = kline['id']

    price = np.array(closed)
    time = np.array(range(2000))

    data = {
        tf.contrib.timeseries.TrainEvalFeatures.TIMES: time,
        tf.contrib.timeseries.TrainEvalFeatures.VALUES: price,
    }

    reader = NumpyReader(data)

    train_input_fn = tf.contrib.timeseries.RandomWindowInputFn(
        reader, batch_size=10, window_size=40)

    ar = tf.contrib.timeseries.ARRegressor(
        periodicities=100, input_window_size=30, output_window_size=10,
        num_features=1,
        loss=tf.contrib.timeseries.ARModel.NORMAL_LIKELIHOOD_LOSS)

    ar.train(input_fn=train_input_fn, steps=500)

    evaluation_input_fn = tf.contrib.timeseries.WholeDatasetInputFn(reader)
    # keys of evaluation: ['covariance', 'loss', 'mean', 'observed', 'start_tuple', 'times', 'global_step']
    evaluation = ar.evaluate(input_fn=evaluation_input_fn, steps=1)

    (predictions,) = tuple(ar.predict(
        input_fn=tf.contrib.timeseries.predict_continuation_input_fn(
            evaluation, steps=1)))

    predictions = float(predictions['mean'].reshape(-1)[0])
    ret = dict()
    ret['prediction'] = float("{0:.2f}".format(predictions))
    ret['cur'] = float("{0:.2f}".format(float(closed[-1])))
    print(ret)
    return jsonify(ret)