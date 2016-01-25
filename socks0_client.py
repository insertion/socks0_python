#!/usr/bin/python3
import socket,select
host="127.0.0.1"
port=9999
sever_address=(host,port)
fd=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
fd.connect(sever_address)
while  1:
	cmd=input("client : ").encode("utf-8")
	#print(cmd)
	if cmd==b'':
		print("don't allow empty,please retry!\n")
		continue
	fd.send(cmd)
	#buff=fd.recv(1024).decode("utf-8")
	#print(buff)
fd.close()
