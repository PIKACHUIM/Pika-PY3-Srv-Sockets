import socket
import hashlib
import time

content = "get test.wav"
server = socket.socket()  # 生成连接
#ip_port = ("vcn1.52pika.iego.net", 4390)  # 地址端口
ip_port = ("127.0.0.1", 1980)  # 地址端口
server.connect(ip_port)  # 连接客户
print("[状态]成功连接...")
while True:
    time.sleep(5)
    server.send(content.encode("utf-8"))              # 传送类型
    server_resp = server.recv(1024)                   # 接收长度
    server_size = int(server_resp.decode("utf-8"))
    print("[状态]接收大小：", server_size)             # 文件内容
    server.send("[状态]准备接收...".encode("utf-8"))   # 确认接收
    server_path = "new" + content.split(" ")[1]
    server_file = open(server_path, "wb")
    receiv_size = 0
    receiv_md5s = hashlib.md5()
    while receiv_size < server_size:
        size = 0  # 解决粘包
        if server_size - receiv_size > 1024:  # 多次接收
            size = 1024
        else:  # 接收完毕
            size = server_size - receiv_size
        data= server.recv(size)  # 多次接收
        data_len = len(data)
        server_file.write(data)
        receiv_md5s.update(data)
        receiv_size += data_len
    print("[状态]成功接收：", int(receiv_size / server_size * 100), "%")
    server_file.close()
    print("[状态]实际接收：", receiv_size)  # 解码
    md5_sever = server.recv(1024).decode("utf-8")
    md5_client = receiv_md5s.hexdigest()
    print("[远程]发来MD5：", md5_sever)
    print("[接收]文件MD5：", md5_client)
    if md5_sever == md5_client:
        print("[成功]MD5值校验")
    else:
        print("[失败]MD5值校验")
server.close()
