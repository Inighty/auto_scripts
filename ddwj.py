# -*- coding: utf-8 -*-
import re
import time
import traceback

from zxtouch.client import zxtouch
from zxtouch.toasttypes import *
from zxtouch.touchtypes import *

device = zxtouch("127.0.0.1")

#device = zxtouch("192.168.0.179")
time.sleep(0.1)


def pprint(data):
    msg = str(data).replace('\'', '"')
    print(msg)
    # device.show_toast(TOAST_SUCCESS, msg, 1.5)
    pass


def back_jd():
    time.sleep(0.1)
    device.switch_to_app("com.360buy.jdmobile")
    time.sleep(1)


def back(x=38, y=66):
    touch(x, y)


def touch(x, y):
    device.touch(TOUCH_DOWN, 1, x, y)
    time.sleep(0.1)
    device.touch(TOUCH_UP, 1, x, y)
    time.sleep(1)


def to_click(arr, pattern, sleep=10, func=None):
    has_task = False

    back_flag = True
    for x in arr:
        if x['text'] == '去完成' or x['text'] == '已完成':
            back_flag = False
            break
        if x['text'] == '残忍离开':
            back(128, 98)
            return True
    if back_flag:
        back()
        return True

    for i, item in enumerate(arr):
        if re.search(pattern, item['text']) and sss[1][i + 1]['text'] == '去完成':
            pprint(item['text'])
            has_task = True
            x = int(sss[1][i + 1]['x'])
            y = int(sss[1][i + 1]['y'])
            touch(x, y)
            time.sleep(sleep)
            if func:
                func()
            back()
            time.sleep(2)
    return has_task


def ocr(languages=None):
    if languages is None:
        languages = ['zh-Hans']
    try:
        return device.ocr((0, 0, 0, 0), languages=languages, recognition_level=0)
    except Exception as e:
        pprint(traceback.format_exc())
        return None


def add_shopcar():
    sss = ocr()
    if sss and sss[0]:
        arr = sss[1]
        for item in arr:
            if item['text'].__contains__('好玩节'):
                x = int(item['x'])
                y = int(item['y'])
                touch(x + 250, y)
                time.sleep(1)
                break


def focus():
    sss = ocr()
    if sss and sss[0]:
        arr = sss[1]
        for item in arr:
            if item['text'].__contains__('关注') and not item['text'].__contains__('人关注'):
                x = int(item['x'])
                y = int(item['y'])
                touch(x, y)
                time.sleep(1)
                break


def open_member():
    sss = ocr()
    if sss and sss[0]:
        arr = sss[1]
        for item in arr:
            if item['text'].__contains__('加入店铺会员'):
                pprint("不自动开会员，如果已开通会员进来只是完成任务，结束脚本")
                exit(0)


def main():
    global sss
    back_jd()
    while True:
        sss = ocr()
        if sss and sss[0]:
            result = sss[1]
            if not to_click(result, '\\d+S'):
                if not to_click(result, '浏览会场', 4):
                    if not to_click(result, '加购', 3, add_shopcar):
                        if not to_click(result, '成功关注', 3, focus):
                            if not to_click(result, '开通品牌会员', 3, open_member):
                                break
            time.sleep(2)

try:
    main()
except Exception as e:
    pprint(traceback.format_exc())