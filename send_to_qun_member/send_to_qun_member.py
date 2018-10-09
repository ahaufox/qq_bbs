# -*- coding:utf8 -*-
from qq_quto_send.fun import functions
import win32gui
import win32api
import time

#QQ窗口前置，用来打开群选择页面
functions.show("QQ")

#定位到好友搜索位置并点击
mov=functions.matchImg('search.png')
win32api.SetCursorPos([mov[0], mov[1]])
functions.left_c()

#定义要搜索的群号码并搜索
qun_id=343371768
functions.setText(qun_id)
time.sleep(2)
mov=functions.matchImg('1.png',0.9)
win32api.SetCursorPos([mov[0]+30, mov[1]+40])
functions.left_dc()
time.sleep(2)

#点击除管理员外的第一个群成员（不含自己）
#需要循环点击
#需要判断点击多少次，如何选择下一个人
mov=functions.matchImg('3.png')
mov=[mov[0]-25, mov[1]+28]
win32api.SetCursorPos([mov[0], mov[1]])
functions.left_dc()
mov[1]=mov[1]+28
time.sleep(2)

win32api.SetCursorPos([mov[0], mov[1]])
mov[1]=mov[1]+28
functions.left_dc()
