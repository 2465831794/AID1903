from socket import *
import os, sys

ADDR = ('127.0.0.1', 8888)


def send_msg(s, name):
    while True:
        text = input("say:")
        if text == 'quit':
            sys.exit("Exit chat room")
        msg = "Q "+name
        s.sendto(msg.encode(),ADDR)

        msg = "C %s %s" % (name, text)
        s.sendto(msg.encode(), ADDR)


def recv_msg(s):
    while True:
        data, addr = s.recvfrom(1025)
        if data.decode() == 'EXIT':
            sys.exit()
        print(data.decode() + "\nsay:",end='')

# 创建网络连接
def main():
    s = socket(AF_INET, SOCK_DGRAM)
    while True:
        name = input("name:")
        msg = "L " + name
        s.sendto(msg.encode(), ADDR)
        # 等待回应
        data, addr = s.recvfrom(1024)
        if data.decode() == "OK":
            print("You have came to chat room")
        else:
            print(data.decode())

        pid = os.fork()
        if pid < 0:
            sys.exit("Error")
        elif pid == 0:
            send_msg(s, name)
        else:
            recv_msg(s)


if __name__ == "__main__":
    main()
