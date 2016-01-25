#!/usr/bin/python3
import socket,select
host ="127.0.0.1"
port = 8989
client=[]
user={}
server_address=(host,port)
fd=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
fd.bind(server_address)
fd.listen(5)
print("server listenning...\n")
while  1:
	infds,outfds,errfds=select.select([fd],[],[],0)
	if infds==[]:
		pass
	else:
		for sock in infds:
			connection,address=sock.accept()
			client.append(connection)
			#accept maybe block,waiting for connect
			print("connection by ",address)
			user[connection]=address

	recvfd,writefd,errfds2=select.select(client,[],[],0)
	if recvfd==[]:
		pass
	else:
		for sock in recvfd:
			buff=sock.recv(1024).decode("utf-8")
			sock.send(b"l have recived your message\n")
			print(user[sock], ":",buff)
			#there will block
			#connection.close()
fd.close()
