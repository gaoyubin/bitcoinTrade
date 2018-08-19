#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-15 15:40:03
# @Author  : KlausQiu
# @QQ      : 375235513
# @github  : https://github.com/KlausQIU

import base64
import hmac
import hashlib
import json

import urllib.request, urllib.parse, urllib.error
import datetime
import requests
import urllib.request, urllib.error, urllib.parse
import urllib.parse

# timeout in 5 seconds:
TIMEOUT = 5

API_HOST = "https://api.hadax.com"

SCHEME = 'https'

# language setting: 'zh-CN', 'en':
LANG = 'zh-CN'

DEFAULT_GET_HEADERS = {
    'Accept':
    'application/json',
    'Accept-Language':
    LANG,
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
}

DEFAULT_POST_HEADERS = {
    'Content-Type':
    'application/json',
    'Accept':
    'application/json',
    'Accept-Language':
    LANG,
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
}
# 此处填写APIKEY

#apple
#ACCESS_KEY = "9e1f2b5e-cdd13dec-bcea6d22-a347f"
#SECRET_KEY = "ef733d65-82540a4b-fb83ba51-eb125"

#nan
#ACCESS_KEY = "7f5c7f68-e39cdc3a-c2b4017f-e03d2"
#SECRET_KEY = "572162df-9d02f7fb-8693e69b-14c24"


#ACCESS_KEY = "075aae5e-8bea2755-71253241-738d8"
#SECRET_KEY = "89040928-6f1d2fb8-347f74f2-71893"

# '''FINAL Keys'''
ACCESS_KEY = "9ec0c479-8a25992c-bc3260f5-e3989"
SECRET_KEY = "4436c80a-010aa1aa-1fec5c26-ab0dc"

# 首次运行可通过get_accounts()获取acct_id,然后直接赋值,减少重复获取。
#ACCOUNT_ID = None
ACCOUNT_ID = 4423693

# API 请求地址
MARKET_URL = TRADE_URL = "https://api.hadax.com"


#各种请求,获取数据方式
def http_get_request(url, params, add_to_headers=None):
    headers = {
        "Content-type":
        "application/x-www-form-urlencoded",
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = urllib.parse.urlencode(params)
    try:
        response = requests.get(
            url, postdata, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "fail"}
    except Exception as e:
        print(("httpGet failed, detail is:%s" % e))
        return {"status": "fail", "msg": e}


def http_post_request(url, params, add_to_headers=None):
    headers = {
        "Accept":
        "application/json",
        'Content-Type':
        'application/json',
        "User-Agent":
        "Chrome/39.0.2171.71",
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = json.dumps(params)
    try:
        response = requests.post(
            url, postdata, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()
    except Exception as e:
        print(("httpPost failed, detail is:%s" % e))
        return {"status": "fail", "msg": e}


def api_key_get(params, request_path):
    method = 'GET'
    print(datetime.datetime.utcnow())
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    print(timestamp)
    params.update({
        'AccessKeyId': ACCESS_KEY,
        'SignatureMethod': 'HmacSHA256',
        'SignatureVersion': '2',
        'Timestamp': timestamp
    })

    host_name = host_url = TRADE_URL
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()

    params['Signature'] = createSign(params, method, host_name, request_path,
                                     SECRET_KEY)
    print(params['Signature'])
    url = host_url + request_path
    return http_get_request(url, params)


def api_key_post(params, request_path):
    method = 'POST'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params_to_sign = {
        'AccessKeyId': ACCESS_KEY,
        'SignatureMethod': 'HmacSHA256',
        'SignatureVersion': '2',
        'Timestamp': timestamp
    }

    host_url = TRADE_URL
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()
    params_to_sign['Signature'] = createSign(params_to_sign, method, host_name,
                                             request_path, SECRET_KEY)
    url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
    return http_post_request(url, params)


def createSign(pParams, method, host_url, request_path, secret_key):
    sorted_params = sorted(list(pParams.items()), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    secret_key = secret_key.encode(encoding='UTF8')
    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature
