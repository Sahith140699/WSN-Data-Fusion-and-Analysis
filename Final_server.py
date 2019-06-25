import socket

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind(('192.168.0.7',3333))
server.listen(5)

while True:
	connection, address = server.accept()
	print("Got connection from",address)
	data = connection.recv(1024)
	print(data)
	connection.close()

