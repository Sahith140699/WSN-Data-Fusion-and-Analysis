import socket
import base64
import numpy as np
import cv2

##Creating the socket
client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
host = '127.0.0.1'
port = 13
client.connect((host,port))

##Recevint the data
data = client.recv(2073600)
print(data)

##Storing the data
fh = open("C:/Users/Sahith/Desktop/IEEE Projects/IEEE Sheet Vision/imageToSave1.png", "wb")
fh.write(base64.b64decode(data))
fh.close()
