#!/usr/bin/env python3

import socket
import sys
import os
import urllib.request

def send_answer(conn, status="200 OK", typ="text/plain; charset=utf-8", data=""):
	data = data.encode("utf-8")
	conn.send(b"HTTP/1.1 " + status.encode("utf-8") + b"\r\n")
	conn.send(b"Server: simplehttp\r\n")
	conn.send(b"Connection: close\r\n")
	conn.send(b"Content-Type: " + typ.encode("utf-8") + b"\r\n")
	conn.send(b"Content-Length: " + bytes(len(data)) + b"\r\n")
	conn.send(b"\r\n")# после пустой строки в HTTP начинаются данные
	conn.sendall(data)



def check_client(conn):
	data = b""
	while not b"\r\n\r\n" in data:
		recieve = conn.recv(1024)
		data += recieve
		
	utf_data = data.decode("utf-8")
	method, address, protocol = utf_data.split(" ", 2)
	print(method, address, protocol)
	
	lst = os.listdir(address)
	
	
	#if 'index.html' not in lst:
	#	send_answer(conn, "404 Not Found", data="404 Not Found")
	#else: 
	#	conn.send(b"HTTP/1.1 200 OK")
		#send_dir_list()
	







#def index_read():
#	f = open("index.html")

##########################################################
if len(sys.argv) == 2:
	try: 
		port = int(sys.argv[1])
	except:
		print("Incorrect port")
		raise
else:
	port = 8000
		
print(port)

serv_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_soc.bind(('', port))
serv_soc.listen(5)



client_soc, client_addr = serv_soc.accept()
print('Connected by', client_addr)

check_client(client_soc)

f = open("test.py")
dat = f.read()

send_answer(client_soc, status="200 OK", typ="file", data=dat)


#client_soc.send(strr)


client_soc.close()
serv_soc.close()









