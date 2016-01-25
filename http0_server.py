#!/usr/bin/python3
import socket
import urllib.parse
Host = '' #symbolic name means all available interface
Port =8989
def server(host,port):
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)#allow port reuse 
	s.bind((Host,Port))
	s.listen(5)
	print("http server is listening...")
	while 1:
		try:
			#print("accept")
			conn,addr=s.accept()
			print(conn,"is Connection")
			handle_connection(conn)
			pass
		except KeyboardInterrupt:
			print("bye...")
			break
		pass

def getline(conn):#if \r\n,return 
	line=''
	while 1:
		#print("read from client")
		buf=conn.recv(1).decode("utf-8")
		#print(buf)
		if buf=='\r':
			line += buf
			#print("come interface")
			buf=conn.recv(1).decode("utf-8")
			#print("endl")
			if buf=='\n':
				#print("huiche")
				line += buf
				return line
				pass
			pass
		else:
			line += buf
		pass
def get_headers(conn):
	headers=''
	while 1:
		line=getline(conn)
		#print(line)
		if line is None:
			break
		if line =="\r\n":
			break
		else:
			headers+=line
		pass
	return headers
	pass
def parse_headers(raw_headers):
	lines=raw_headers.split("\r\n")
	request_line=lines[0].split(' ')
	method=request_line[0]
	full_path=request_line[1]#broswer generate if use proxy,different normal modle
	version=request_line[2]
	print("%s %s"%(method,full_path))
	(scm,netloc,path,params,query,fragment)=urllib.parse.urlparse(full_path,"http")
	i=netloc.split(':')
	#print("i is ",i,len(i))
	if len(i)==2:
		address=i[0],int(i[1])
	else:
		address=i[0],80
	return method,version,scm,address,path,params,query,fragment
	pass
def handle_connection(conn):
	req_headers=get_headers(conn)
	if req_headers is None:
		return
	method,version,scm,address,path,params,query,fragment=parse_headers(req_headers)
	path=urllib.parse.urlunparse(["","",path,params,query,""])
	req_headers=' '.join([method,path,version])+"\r\n"+"\r\n".join(req_headers.split("\r\n")[1:])
	#create socket
	soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print("connect",address)
	soc.connect(address)
	if req_headers.find("Connection")>=0:
		req_headers = req_headers.replace("keep-alive","close")
	else:
		req_headers+=req_headers+"Connection:close\r\n"
	req_headers+="\r\n"
	soc.sendall(req_headers.encode("utf-8"))

	#read from server
	data=b''
	while 1:
		#print("read from server")
		buf=soc.recv(8129)
		data+=buf
		if not len(buf):
			soc.close()
			break
	conn.sendall(data)
	conn.close()
	print(conn,"is close")

if __name__ == '__main__':
	server(Host,Port)