import sys
import time
from socket import *
from time import sleep


class FTPClient:
    def __init__(self, sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b'L')
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            while True:
                data = self.sockfd.recv(4096)
                if data == b'##':
                    print(data.decode())
        else:
            print(data)

    def do_quit(self):
        self.sockfd.send(b'Q')
        self.sockfd.close()
        sys.exit("Thank you")

    def do_get(self, file_name):
        self.sockfd.send(('G ' + file_name).encode())
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            fd = open(str(file_name), 'wb')
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    break
                fd.write(data)
            fd.close()
        else:
            print(data)

    def do_put(self,file_name):
        try:
            fd = open(file_name, 'rb')
        except Exception:
            print("didn't had")
            return
        file_name = file_name.split('/')[-1]
        self.sockfd.send(('P '+file_name).encode())
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            while True:
                data = fd.read(1024)
                self.sockfd.send(data)
                if not data:
                    time.sleep(0.1)
                    self.sockfd.send(b'##')
                    break
                self.sockfd.send(data)
            fd.close()
        else:
            print(data)


def request(sockfd):
    ftp = FTPClient(sockfd)
    while True:
        print("========命令选项========")
        print("========list==========")
        print("=======get_file=======")
        print("=======put_file=======")
        print("=========quit=========")
        print()
        cmd = input("输入命令")
        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd.strip() == 'quit':
            ftp.do_quit()
        elif cmd[:3] == 'get':
            filename = cmd.strip().split(' ')[-1]
            ftp.do_get(filename)
        elif cmd[:3] == 'put':
            filename = cmd.strip().split(' ')[-1]
            ftp.do_put(filename)


def main():
    ADDR = ('127.0.0.1', 8888)
    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except KeyboardInterrupt:
        sockfd.close()
        return
    except Exception as e:
        print("sorry")
        return
    else:
        print("------------------"
              "Data   File  Image"
              "------------------")
        cls = input("请输入文件种类:")
        if cls not in ["Data", "File", "image"]:
            print("sorry input Error")
            return
        else:
            sockfd.send(cls.encode())
            request(sockfd)


if __name__ == "__main__":
    main()
