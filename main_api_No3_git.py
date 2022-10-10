# -*- coding: utf-8 -*-
import sys
import uuid
import hashlib
from importlib import reload
import win32clipboard as w
import win32con
import requests
import time

reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '你的密钥id'
APP_SECRET = '你的密钥'


def getText():  # 读取剪切板
    # 打开剪贴板
    w.OpenClipboard()
    # 读取剪贴板的内容
    d = w.GetClipboardData(win32con.CF_UNICODETEXT)
    # 关闭剪贴板
    w.CloseClipboard()
    return d



def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect(q):
    # q = "でﾓ､クライブがｺﾉ世界ﾆ来ﾅｹﾚば"

    data = {}
    data['from'] = 'ja'
    data['to'] = 'zh-CHS'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign
    data['vocabId'] = ""

    response = do_request(data)
    print(response.json()['translation'][0])


if __name__ == '__main__':
    lj = ''
    # 主循环，开始不停获取翻译
    while True:
        time.sleep(1)
        try:
            xj = getText()
            if xj != lj:
                connect(xj)
                # print(res)

            lj = xj
        except:
            print("jterror")


