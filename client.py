import socket
import os
import hashlib

client = socket.socket()
client.bind(("127.0.0.1", 1980))             # 地址端口
client.listen(5)
print("[状态]等待连接...")
while True:
    conn, addr = client.accept()             # 等待连接
    print("[地址]", addr)                    # 连接实例
    while True:
        data = conn.recv(1024)               # 接收指令
        if not data:                         # 断开连接
            print("[状态]断开连接...")
            break
        print("[状态]收到命令：", data.decode("utf-8"))
        cmd, filename = data.decode("utf-8").split(" ")
        if cmd == "get":
            if os.path.isfile(filename):          # 判断文件存在
                size = os.stat(filename).st_size  # 获取文件大小
                conn.send(str(size).encode("utf-8"))  # 发送数据长度
                print("[状态]发送大小：", size)
                conn.recv(1024)                       # 接收确认
                md5s = hashlib.md5()
                file = open(filename, "rb")
                for line in file:
                    conn.send(line)                       # 发送数据
                    md5s.update(line)
                file.close()
                md5g = md5s.hexdigest()
                conn.send(md5g.encode("utf-8"))
                print("[状态]MD5值：", md5g)
client.close()
