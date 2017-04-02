#!/usr/bin/env python3

import socket
import sys
import os
import urllib.request
import time


def get_port():
	if len(sys.argv) == 2:
		try:
			port = int(sys.argv[1])
			if port not in range(1024,65536):
				print("Port out of range!")
				raise SystemExit
			else:
				return port
		except:
			print("Incorrect input")
			raise
	else:
		return 8000


def send_answer(conn, status="200 OK", typ="text/plain; charset=utf-8", data=""):
	data = data.encode("utf-8")
	conn.send(b"HTTP/1.1 " + status.encode("utf-8") + b"\r\n")
	conn.send(b"Server: simplehttp\r\n")
	conn.send(b"Connection: close\r\n")
	conn.send(b"Content-Type: " + typ.encode("utf-8") + b"\r\n")
	conn.send(b"Content-Length: " + bytes(len(data)) + b"\r\n")
	conn.send(b"\r\n")
	conn.sendall(data)



def check_client(conn, addr):
	data = b""
	while not b"\r\n\r\n" in data:
		recieve = conn.recv(1024)
		data += recieve

	utf_data = data.decode("utf-8")

	method, address, params = utf_data.split(" ", 2)
	protocol, params = params.split("\r\n", 1)

	conn_time = time.strftime("[%d/%b/%G %H:%M:%S]")
	print("%s - - %s \"%s %s %s\" 200 -" % (addr, conn_time ,method, address, protocol))
	#print(params)

	check_path(conn, address)
	conn.close()

def check_path(conn, path):
	work_dir = os.getcwd()
	#print(work_dir + path)

	if os.path.isdir(work_dir + path):
		#print(work_dir + path + "CONTACT")
		for index in "/index.html", "/index.htm":
			if os.path.isfile('.' + path + index):
				f = open(os.path.normpath('.' + path + index))
				send_answer(conn, typ="text/html", data=f.read())
			else:
				send_answer(conn)
			break

	elif os.path.isfile('.' + path):
		f = open('.' + path)
		send_answer(conn, typ="text/html", data=f.read())
	else:
		send_answer(conn, "404 Not Found", data="Не найдено")



#def index_read():
#	f = open("index.html")
#send_answer(conn, status="302 Moved Temporarily", loc="localhost:8000/index.html"
#conn.send(b"Location: " + loc.encode("utf-8")+ b"\r\n")
##########################################################
port = get_port()

serv_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_soc.bind(('', port))
serv_soc.listen(5)

print("Serving HTTP on %s port %d ..." % serv_soc.getsockname())

try:
	while True:
		client_soc, client_addr = serv_soc.accept()
		try:
			check_client(client_soc, client_addr[0])

		except:
			send_answer(client_soc, status="500", typ="500 Internal Server Error", data="500 Internal Server Error")
			raise
		finally:
			client_soc.close()
except KeyboardInterrupt:
	print("KeyboardInterrupt")
finally:
	serv_soc.close()
