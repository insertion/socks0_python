#!/usr/bin/python3
import socket,select
server_address=("localhost",8888)
proxy_address=("localhost",8989)
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen(10)
print("listenning...\n")
client=[sock]
user={}
while 1:
	infds,out,err=select.select(client,[],[])
	for x in infds:
		if x==sock:
			connection,addre=x.accept()
			client.append(connection)
			fd=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			fd.connect(proxy_address)
			client.append(fd)
			user[connection]=fd
			user[fd]=connection
		else:
			buff=x.recv(8096)
			print(buff)
			#user[x].sendall(buff)
	pass
