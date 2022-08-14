"""
    Chat room
"""

from socket import *
import os, sys

ADDR = ('0.0.0.0', 8888)
user = {}


def do_login(s, name, addr):
    if name in user or "controller" in name:
        s.sendto("\nThe user have sat",addr)
        return
    s.sendto(b'OK', addr)

    # 通知其他人
    msg = "\nWelcom %s" % name
    for i in user:
        s.sendto(msg.encode(), user[i])
    # 将用户加入
    user[name] = addr


def do_chat(s, name, text):
    msg = "\n%s:  %s" % (name, text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])


def do_quit(s, name):
    msg = "\n%s exit chat room" % name
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])
        else:
            s.sendto(b'EXIT', user[i])
    del user[name]


# 接受客户端请求
def do_request(s):
    while True:
        data, addr = s.recvfrom(1024)
        print(data.decode())
        msg = data.decode().split(' ')

        if msg[0] == 'L':
            do_login(s, msg[1], addr)
        elif msg[0] == 'C':
            text = " ".join(msg[2:])
            do_chat(s, msg[1], text)
        elif msg[0] == 'Q':
            if msg[1] not in user:
                s.sendto(b'EXIT',addr)
                continue
            do_quit(s, msg[1])


# 创建网络连接
def main():
    # 套接字
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)
    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        while True:
            msg = input("\ncontroller message")
            msg = "\nC controller:" + msg
            s.sendto(msg.encode(),ADDR)
    else:
        do_request(s)


if __name__ == "__main__":
    main()
