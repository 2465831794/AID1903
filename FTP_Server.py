import os
from socket import *
from threading import Thread
from time import sleep

HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST, PORT)
FTP = "/home/ftw/FTP/"


class FTPServer:
    def __init__(self, connfd, FTP_PATH):
        self.connfd = connfd
        self.path = FTP_PATH

    def do_list(self):
        files = os.listdir(self.path)
        if not files:
            print("该文件类别为空")
            return
        else:
            self.connfd.send(b'OK\n')
        fs = ''
        for file in files:
            if file[0] != '.' and os.path.isfile(self.path + file):
                fs += '%s\n' % file
        self.connfd.send(fs.encode())

    def do_get(self, file_name):
        try:
            fd = open(self.path+file_name, 'rb')
        except Exception as e:
            self.connfd.send("didn't have".encode())
            return
        else:
            self.connfd.send(b'OK')
            sleep(0.1)
        while True:
            data = fd.read(1024)
            if not data:
                sleep(0.1)
                self.connfd.send(b'##')
                break
            self.connfd.send(data)

    def do_put(self, file_name):
        if os.path.exists(self.path+file_name):
            self.connfd.send("you have this file".encode())
            return
        self.connfd.send(b'OK')
        fd = open(self.path + file_name,'wb')
        while True:
            data = self.connfd.recv(1024)
            if data == b'##':
                break
            fd.write(data)
        fd.close()


def handle(connfd):
    cls = connfd.recv(1024).decode()
    FTP_PATH = FTP + cls + '/'
    ftp = FTPServer(connfd, FTP_PATH)
    while True:
        data = connfd.recv(1024).decode()
        if not data or data[0] == 'Q':
            return
        elif data[0] == 'L':
            ftp.do_list()
        elif data[0] == 'G':
            filename = data.split(' ')[-1]
            ftp.do_get(filename)
        elif data[0] == 'P':
            filename = data.split(' ')[-1]
            ftp.do_put(filename)


def main():
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(3)
    print("Listen the port 8888...")
    while True:
        try:
            connfd, addr = sockfd.accept()
        except KeyboardInterrupt:
            print("bye")
            return
        except Exception as e:
            print(e)
            continue
        print("Client:", addr)
        client = Thread(target=handle, args=(connfd,))
        client.setDaemon(True)
        client.start()


if __name__ == "__main__":
    main()
