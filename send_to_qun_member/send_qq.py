# -*- coding:utf8 -*-
from PIL import ImageGrab
import aircv as ac
import win32gui
from win32gui import *
import win32con
import win32api
import time
import win32clipboard as w
import requests
import re
import pyperclip
import pymysql
import random
from ctypes import *
import pyautogui as pag
#############base functions##################
#匹配图片
def matchImg(imgsrc, confidencevalue=0.95):
    im = ImageGrab.grab()
    x='cap.png'
    im.save(x, 'png')
    imsrc = ac.imread(imgsrc)
    imobj = ac.imread(x)
    match_result = ac.find_template(imsrc, imobj)
    if match_result is not None:
        match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽
        match_result['click']=(int(match_result['rectangle'][0][0]+match_result['shape'][0]/2),int(match_result['rectangle'][0][1]+match_result['shape'][1]/2))
        mov = match_result['click']
        return mov
    else:
        return 1

#左键单击
def left_c():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

# 左键双击
def left_dc():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    return

#粘贴录入的内容
def setText(aString):
    aString=str(aString)
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardText(aString)
    w.CloseClipboard()
    win32api.keybd_event(17, 0, 0, 0)
    win32api.keybd_event(86, 0, 0, 0)
    time.sleep(0.4)
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(8, 0, 0, 0)
    time.sleep(0.4)
    win32api.keybd_event(8, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.5)
    win32api.keybd_event(17, 0, 0, 0)
    win32api.keybd_event(90, 0, 0, 0)
    time.sleep(0.4)
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(90, 0, win32con.KEYEVENTF_KEYUP, 0)
    return



def get_bkn(cookies):
    list = cookies.split('; ')
    hash = 5381
    dis_qq = {}
    for i in range(0, len(list)):
        try:
            for i in range(0, len(list)):
                dis_qq[list[i].split('=')[0]] = list[i].split('=')[1]
        except IndexError:
            return IndexError
        else:
            skey = dis_qq['skey']
            qq_id = re.findall('[1-9][0-9]{4,}', dis_qq['uin'])
            for i in range(len(skey)):
                hash += (hash << 5) + ord(skey[i])
                i += 1
            bkn = hash & 2147483647
            return [qq_id, bkn]

def get_cookies(cookies):
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'content-type': 'text/html; charset=utf-8',
        'Referer': 'https://qun.qq.com/member.html',
        'Cookie': cookies
    }
    url_chkec = 'https://qun.qq.com/cgi-bin/qun_mgr/get_group_list'
    bkn = get_bkn(cookies)
    try:
        data = {
            'bkn': bkn[1]
        }
    except:
        return 'data err'
    req = requests.post(url_chkec, data=data, headers=headers)
    content = req.json()
    # return content
    if content['ec'] == 0:
        return (content)
    else:
        cookies = input("需要重新登陆,输入账号{}的cookies：".format(id))
        list = cookies.split('; ')
        try:
            dis_qq = {}
            for i in range(0, len(list)):
                dis_qq[list[i].split('=')[0]] = list[i].split('=')[1]
        except:
            print("输入有误，重新输入")
            cookies = input("需要重新登陆,输入账号{}的cookies：".format(id))
            list = cookies.split('; ')
            try:
                dis_qq = {}
                for i in range(0, len(list)):
                    dis_qq[list[i].split('=')[0]] = list[i].split('=')[1]
            except:
                return "输入有误，重新运行程序"
        print("处理中……")

def mysql_local_select(sql):
    try:
        conn = pymysql.connect(host='192.168.1.114',
                               port=3306,
                               user='root',
                               password='root',
                               db='qq_send',
                               charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
    except pymysql.Error as e:
        return e
    else:
        try:
            cur.execute(sql)
            re=cur.fetchall()
            cur.close()
            conn.close()
        except conn.Error as e:
            return e
        else:
            return re

def mysql_local_update_insert(sql):
    try:
        conn = pymysql.connect(host='192.168.1.114',
                               port=3306,
                               user='root',
                               password='root',
                               db='qq_send',
                               charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
    except pymysql.Error as e:
        return e
    else:
        try:
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
        except conn.Error as e:
            return e
        else:
            return 1

def mov(m,n):
    block()
    win32api.SetCursorPos([m, n])
    left_c()
    disblock()

#判断特定id的cookies是否有效
#若无效：提示原因并更新
#若有效，返回群数组（不含自己创建的）
def check_cookies(qq_id):
    res=mysql_local_select('select cookies from qq_send_cookies where qq_id={}'.format(qq_id))
    if res==():
        update_cookies(qq_id)
    else:
        cookies=res[0]['cookies']
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'content-type': 'text/html; charset=utf-8',
        'Referer': 'https://qun.qq.com/member.html',
        'Cookie': cookies
    }
    url_check = 'https://qun.qq.com/cgi-bin/qun_mgr/get_group_list'
    get_bkn_res = get_bkn(cookies)
    bkn = get_bkn_res[1]
    id_need = int(get_bkn_res[0][0])
    id_list = []
    if id_need == qq_id:
        try:
            data = {
                'bkn': bkn
            }
        except:
            return 'data err'
        req = requests.post(url_check, data=data, headers=headers)
        content = req.json()
        if content['ec'] == 0:
            id_list.append([qq_id, cookies])
        else:
            # 更新cookies
            cookies = input("输入 {} 的 cookies：".format(qq_id))
            try:
                list = cookies.split('; ')
                dis_qq = {}
                for i in range(0, len(list)):
                    dis_qq[list[i].split('=')[0]] = list[i].split('=')[1]
            except:
                print ("格式有误，重新输入")
                cookies = input("重新输入{}的 cookies：".format(qq_id))
                try:
                    list = cookies.split('; ')
                    dis_qq = {}
                    for i in range(0, len(list)):
                        dis_qq[list[i].split('=')[0]] = list[i].split('=')[1]
                except:
                    print ("又输入错了，直接关了程序，然后再开一下！")
                    return 1
            else:
                print ("处理中……")
            sql_update = """update qq_send_cookies set cookies=\"{}\",qq_id={}""".format(cookies,qq_id)
            if mysql_local_update_insert(sql_update) == 1:
                return "数据写入成功，需再次执行程序！"
            else:
                return "数据写入错误，联系程序员！"
        return content['join']  # cookies验证没问题，自动返回list
    else:
        print ("帐号和cookies不对应！")
        cookies = input("需要重新登陆,输入账号{}的cookies：".format(qq_id))
        try:
            list = cookies.split('; ')
            dis_qq = {}
            for i in range(0, len(list)):
                dis_qq[list[i].split('=')[0]] = list[i].split('=')[1]
        except:
            print ("wrong,try again!")
            cookies = input("input {}`s cookies again：".format(qq_id))
            try:
                list = cookies.split('; ')
                dis_qq = {}
                for i in range(0, len(list)):
                    dis_qq[list[i].split('=')[0]] = list[i].split('=')[1]
            except:
                print ("input {}`s cookies again：")
                return 1
        print ("处理中……")
        sql_update = """update qq_send_cookies set cookies=\"{}\" , qq_id={}""".format(cookies,qq_id)
        s=mysql_local_update_insert(sql_update)

        if s== 1:
            print ("数据写入成功，需再次执行程序！")
            return
        else:
            print ("数据写入错误，联系程序员！")
            return

def update_cookies(qq_id):
    return

#禁用鼠标键盘
def block():
    windll.LoadLibrary('user32.dll').BlockInput(True)

def disblock():
    windll.LoadLibrary('user32.dll').BlockInput(False)
#############base functions over##################


def insert_qunid(qun_id,id):
    sql='insert into qq_send_qun set qun_id={},down=0,from_qq={}'.format(qun_id,id)
    res = mysql_local_update_insert(sql)
    return res

def check_never_send(qun_id):
    sql='select * from qq_send_never_send where qun_id={}'.format(qun_id)
    res=mysql_local_select(sql)
    if res==():
        return 0
    else:
        return 1

def get_qun_id(qq_id):
    content=check_cookies(qq_id)
    for i in range(0,len(content)):
        if check_never_send(int(content[i]['gc']))==1:
            pass
        else:
            insert_qunid(content[i]['gc'],qq_id)
    return

#返回数组集合 qq id list
def get_member_id(qun_id):
    sql='select from_qq from qq_send_qun where qun_id={} and down=0'.format(qun_id)
    res=mysql_local_select(sql)
    if res==():
        return 'nothing to do'
    else:
        qq_id=res[0]['from_qq']
    sql='select cookies from qq_send_cookies where qq_id={}'.format(qq_id)
    cookies=mysql_local_select(sql)[0]['cookies']
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'content-type': 'text/html; charset=utf-8',
        'Referer': 'https://qun.qq.com/member.html',
        'Cookie': cookies
    }
    url = 'https://qun.qq.com/cgi-bin/qun_mgr/search_group_members'
    get_bkn_res = get_bkn(cookies)
    bkn = get_bkn_res[1]
    try:
        data = {
            'gc': qun_id,
            'st': 0,
            'end': 0,
            'bkn': bkn
        }
    except:
        return 'data err'
    request = requests.post(url=url, data=data, headers=headers)
    res_json = request.json()
    if res_json['ec'] != 0:
        return
    else:
        s = res_json['count']
        data = {
            'gc': qun_id,
            'st': 0,
            'end': s,
            'bkn': bkn
        }
        request = requests.post(url=url, data=data, headers=headers)
        res_json = request.json()
        member_list = res_json['mems']
        for i in range(0, len(member_list)):
            if member_list[i]['role']==0 or member_list[i]['role']==1:
                pass
            else:
                uin = member_list[i]['uin']
                sql = """insert into qq_send_send set qq_id={},from_qq={}""".format(uin, qq_id)
                mysql_local_update_insert(sql)
    return

def insert_all_qq(qq_id):
    sql="""select qun_id from qq_send_qun where down=0 and from_qq={}""".format(qq_id)
    res=mysql_local_select(sql)
    if res==():
        return 'nothing to do'
    else:
        for i in res:
            get_member_id(i['qun_id'])
    return

def show(X):
    titles = set()
    def foo(hwnd, mouse):
        if IsWindow(hwnd) and IsWindowEnabled(hwnd):
            titles.add(GetWindowText(hwnd))
    EnumWindows(foo, 0)
    lt = [t for t in titles if t]
    lt.sort()
    for t in lt:
        tt = win32gui.FindWindow(None, t)
        if t == X:
            h = tt
            win32gui.ShowWindow(h, win32con.SW_SHOWDEFAULT)
            win32gui.SetForegroundWindow(h)
        else:
            pass
    return

def get_post_content():
    sql='select content from qq_send_content'
    res=mysql_local_select(sql)
    x=random.randint(1, len(res))-1
    res=res[x]['content']
    return res

def get_post_id(qq_id):
    sql='select qq_id from qq_send_send where down=0 and from_qq ={} limit 10 '.format(qq_id)
    res = mysql_local_select(sql)
    if res==():
        return
    else:
        x = random.randint(0, len(res)-1)
        return res[x]['qq_id']

def rember_post(content,post_time,qq_id):
    sql='update qq_send_send set down=1,post_content=\"{}\",post_time={} where qq_id={}'.format(content,post_time,qq_id)
    res=mysql_local_update_insert(sql)
    return res

def update_qun_and_qq(qq_id):
    get_qun_id(qq_id)
    insert_all_qq(qq_id)

def is_ok():
    xx, yy = pag.position()
    m1=matchImg('dai.png',1)
    if m1 == 1:
        pass
    else:
        m1 = matchImg('cancel.png', 0.95)
        if m1==1:
            pass
        else:
            x, y = pag.position()
            block()
            mov(m1[0], m1[1])
            left_c()
            mov(x,y)
            disblock()
    m2=matchImg('dis_alow.png',1)
    if m2==1:
        pass
    else:
        m2 = matchImg('cancel.png',0.95)
        if m2==1:
            pass
        else:
            x, y = pag.position()
            block()
            mov(m2[0], m2[1])
            left_c()
            mov(x, y)
            disblock()
    m3=matchImg('add.png',1)
    if m3==1:
        pass
    else:
        m3 = matchImg('cancel.png',0.95)
        if m3==1:
            pass
        else:
            x, y = pag.position()
            block()
            mov(m3[0], m3[1])
            left_c()
            mov(x, y)
            disblock()
    mov(xx,yy)
    return

def send_ad(qq_ned):
    # 打开qq
    show('QQ')
    setText(qq_ned)
    # 检测QQ是否找到
    time.sleep(0.2)
    for i in range(0,6):
        move = matchImg('other_friend.png')
        if move==1:
            if i==5:
                return
            else:
                time.sleep(0.2 * i)
                pass
        else:
            mov(move[0] + 30, move[1] + 40)
            time.sleep(0.2)
            left_dc()
            break
    # 随机取需要发送的内容
    content = get_post_content()
    for i in range(1,5):
        move = matchImg('left.png')
        if move==1:
            time.sleep(0.1 * i)
            pass
        else:
            block()
            mov(move[0],move[1])
            time.sleep(0.5)
            left_c()
            disblock()
            break
    setText(content)
    time.sleep(0.2)
    win32api.keybd_event(13, 0, 0, 0)  # 回车
    time.sleep(0.2)
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)  # Realiz
    is_ok()
    for i in range(1,5):
        move = matchImg('shout_down.png')
        if move==1:
            time.sleep(0.1 * i)
            pass
        else:
            block()
            mov(move[0],move[1])
            time.sleep(0.5)
            left_c()
            disblock()
            break
    rember_post(content, int(time.time()), qq_ned)
    print(qq_ned)
    return

def send_qq(qq_id,times):
    time.sleep(1)
    for i in range(0,times):
        # 拿需要的QQ号
        qq_ned = get_post_id(qq_id)
        if qq_ned is None:
            print('所有QQ均已发送')
            return
        else:
            send_ad(qq_ned)
    return 'all down!'
#check_cookies(547575116)
#update_qun_and_qq(547575116)
#insert_all_qq(547575116)
#send_qq(452193182, 5000)
#
for i in range(0,10):
    try:
        send_qq(452193182,5000)
    except:
        print ("err")
    else:
        send_qq(452193182, 5000)
