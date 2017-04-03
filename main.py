#!/usr/bin/env python3

import socket
import sys
import os
import urllib.request
import time

def gen_err_page(err_code='404', mess=' ', err_code_expln=' '):
	err_page = "<!DOCTYPE html><html><head>"
	err_page += "<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\">"
	err_page += "<title>Error response</title></head><body>"
	err_page += "<h1>Error response</h1>"
	err_page += "<p>Error code: {:s}</p>".format(err_code)
	err_page += "<p>Message: {:s}.</p>".format(mess)
	err_page += "<p>Error code explanation: {:s}.</p>".format(err_code_expln)
	err_page += "</body></html>"
	return err_page

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
	conn.send(b"\r\n\r\n")
	conn.sendall(data)


def check_client(conn, client_addr):
	data = b""
	while not b"\r\n" in data:
		recieve = conn.recv(1024)
		if not recieve:
			break
		else:
			data += recieve
	if not data:
		return

	#print(data)
	utf_data = data.decode("utf-8")
	request = utf_data.split("\r\n", 1)[0]
	method, uri, protocol = request.split(" ", 2)
	conn_time = time.strftime("[%d/%b/%G %H:%M:%S]")
	print("%s - - %s \"%s %s %s\" ---" % (client_addr, conn_time ,method, uri, protocol)) #end=' '
	if method == "GET":
		check_path(conn, uri)
	else:
		return

def open_index(conn, path):
	for item in ["/index.html", "/index.htm"]:
		if os.path.isfile('.' + path + item):
			with open(os.path.normpath('.' + path + item)) as textfile:
				return textfile.read()
	else:
		return False

def check_path(conn, path):
	work_path = os.getcwd()
	if os.path.isdir('.' + path):
		index = open_index(conn, path)
		status = "200 OK"
		print("zashlo")
		if not index:
			data = gen_list_dir(path)
		else:
			data = index
	elif os.path.isfile('.' + path):
		##############################################
		print(">>><<<<")##############################
	else:
		status = "404 Not Found"
		data = gen_err_page("404 Not Found")

	send_answer(conn, status=status, typ="text/html;charset=utf-8", data=data)


def gen_list_dir(path):
	items = os.listdir('.' + path)
	print(items)
	items.sort(key=lambda a: a.lower())

	page = "<!DOCTYPE html><html><head>"
	page += "<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\">"
	page += "<title>Directory listing for {0:s}</title></head>".format(path)
	page += "<body><h1>Directory listing for {0:s}</h1><hr><ul>".format(path)

	for item in items:
		page += "<li><a href=\"{0:s}\">{0:s}</a></li>".format(item)
	page += "</ul><hr></body></html>"
	return page




###############################################################################
port = get_port()
serv_sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sck.bind(('', port))
serv_sck.listen(10)

print("Serving HTTP on %s port %d ..." % serv_sck.getsockname())

try:
	while True:
		client_sck, client_addr = serv_sck.accept()
		try:
			check_client(client_sck, client_addr[0])

		#except:
			#send_answer(client_sck, "500 Internal Server Error", data="500 Internal Server Error")
		finally:
			client_sck.close()
except KeyboardInterrupt:
	print("KeyboardInterrupt")
finally:
	serv_sck.close()
