
import socket
import cv2
import numpy as np
import base64


##Read the image and convert into base64 format
with open("C:/Users/Sahith/Desktop/IEEE Projects/IEEE Sheet Vision/IR Sensor circuit.png", "rb") as imageFile:
    img_str = base64.b64encode(imageFile.read())
    print(type(img_str))
    print(img_str)

##Create server
server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind(('127.0.0.1', 13))
server.listen(5)

##Connect to client and Send the image
while True:
    connection,address = server.accept()
    print('Got connection from', address)
    connection.send(img_str)
    connection.close()  # close the connection




