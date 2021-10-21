# -*- coding: utf-8 -*-
import re

from zxtouch.client import zxtouch
from zxtouch.toasttypes import *
from zxtouch.touchtypes import *

back_x_y = (38, 66)
close_x_y = (128, 98)
ip = "192.168.0.141"


def sleep(seconds):
    device.accurate_usleep(seconds * 1000000)


device = zxtouch(ip)
sleep(0.1)


def pprint(data):
    msg = str(data).replace('\'', '"')
    # print(msg)
    device.show_toast(TOAST_SUCCESS, msg, 1.5)
    pass


def back_jd():
    sleep(3)
    device.switch_to_app("com.360buy.jdmobile")
    sleep(1)


def back():
    touch(back_x_y[0], back_x_y[1])


def touch(x, y):
    device.touch(TOUCH_DOWN, 1, x, y)
    sleep(0.001)
    device.touch(TOUCH_UP, 1, x, y)
    sleep(1)


def to_click(arr, pattern, sleep_sec=10, func=None):
    has_task = False

    back_flag = True
    for x in arr:
        if x['text'] == '去完成' or x['text'] == '已完成':
            back_flag = False
            break
        if x['text'] == '残忍离开':
            touch(close_x_y[0], close_x_y[1])
            return True
    if back_flag:
        back()
        return True

    for i, item in enumerate(arr):
        if re.search(pattern, item['text']):
            left = int(item['y'])
            right = None
            for j, itemj in enumerate(arr):
                tt = itemj['text']
                if tt == '去完成' and left - 50 < int(itemj['y']) < left + 50:
                    right = itemj
                    break
            if right:
                has_task = True
                pprint(item['text'])
                x = int(right['x'])
                y = int(right['y'])
                touch(x, y)
                sleep(sleep_sec)
                if func:
                    func()
                sleep(2)
                break
    return has_task


def scan():
    back_jd()


def ocr(languages=None):
    if languages is None:
        languages = ['zh-Hans']
    return device.ocr((0, 0, 0, 0), languages=languages, recognition_level=0)


def add_shopcar():
    sss = ocr(['english'])
    if sss and sss[0]:
        arr = sss[1]
        for item in arr:
            if item['text'].__contains__('11.11'):
                x = int(item['x'])
                y = int(item['y'])
                touch(x + 250, y)
                sleep(1)
                back()
    back()


def focus():
    sss = ocr()
    if sss and sss[0]:
        arr = sss[1]
        for item in arr:
            if item['text'].__contains__('关注') and not item['text'].__contains__('人关注'):
                x = int(item['x'])
                y = int(item['y'])
                touch(x, y)
                sleep(1)
                break
    back()


def open_member():
    sss = ocr()
    if sss and sss[0]:
        arr = sss[1]
        is_open = True
        for item in arr:
            if item['text'].__contains__('确认授权即同意'):
                is_open = False
                touch(int(item['x']) - 30, int(item['y']) + 20)
            if item['text'].__contains__('确认授权并加入店铺会员'):
                is_open = False
                touch(int(item['x']), int(item['y']))
        if is_open:
            back()
        sleep(2)


def main():
    global sss
    while True:
        sss = ocr()
        if sss and sss[0]:
            result = sss[1]
            if not any(re.search('累计任务奖励', item['text']) for item in result):
                pprint("please go to the start page.")
                sleep(2)
                continue
            if not to_click(result, '成功入会', 4, open_member):
                if not to_click(result, '.*浏览并关注.*|.*浏览可得.*|.*浏览\\d+.*', 10, back):
                    if not to_click(result, '.*浏览即可得.*', 3, back):
                        if not to_click(result, '累计浏览', 3, add_shopcar):
                            if not to_click(result, '成功关注', 3, focus):
                                break
            sleep(2)


main()
device.disconnect()
