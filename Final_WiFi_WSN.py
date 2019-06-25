import cv2
import numpy as np
import time
import os
import requests
from picamera import PiCamera
import socket


url1 = 'http://192.168.0.4:8090/rest/things/hue%3A0210%3A001788afee6e%3A2'
path = "/home/pi/train/"
client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
host = '192.168.0.7'
port = 3333

images = []
for i in os.listdir(path):
	im = cv2.imread(path + i,1)
	im = np.float32(im)/255
	images.append(im)
	imFlip = cv2.flip(im,1)
	images.append(imFlip)

numImages = len(images)
sz = images[0].shape
print(sz)
data = np.zeros((numImages, sz[0]*sz[1]*sz[2]), dtype = np.float32)
for i in range(0,numImages):
	image = images[i].flatten()
	data[i,:] = image
print(data)

NUM_EIGEN_FACES = 10
print("Calculating PCA",end="...")
mean,eigenVectors = cv2.PCACompute(data, mean=None, maxComponents = NUM_EIGEN_FACES)
print("Done")
averageFace = mean.reshape(sz)

eigenFaces = []
for eigenVector in eigenVectors:
	eigenFace = eigenVector.reshape(sz)
	eigenFaces.append(eigenFace)

output = cv2.resize(averageFace, (0,0),fx=2,fy=2)
#cv2.imshow("Average",output)
#print(output)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

weights = []

for i in os.listdir(path):
	print(i)
	im = cv2.imread(path + i,1)
	im = np.float32(im)/255
	imVector = im.flatten() - mean
	output = averageFace
	temp = []
	for i in range(0,len(eigenVectors)):
		weight = np.dot(imVector, eigenVectors[i])
		temp.append(weight[0])
	print(temp)
	weights.append(temp)

camera = PiCamera()
status = "\"ONLINE\""
def face_detection():
	try:
		face_cascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
		img = cv2.imread('/home/pi/Desktop/image.png')
		faces = face_cascade.detectMultiScale(img, 1.3, 5)
		if(len(faces) != 0):
			print("Face Detected")
			Classification(faces)
		else:
			print("No person detected")
	except Exception as e:
		print(e)
def Classification(*faces):
	try:
		img = cv2.imread('/home/pi/Desktop/image.png')
		print("Classification Started")
		for (x,y,w,h) in faces[0]:
			print(x,y,w,h)
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
			img_face = img[y:y+h, x:x+w]
		img_face_r = cv2.resize(img_face,(100,100),cv2.INTER_LINEAR)
		img_face_r = np.float32(img_face_r)/255.0
		img_vector = img_face_r.flatten() - mean
		t = []
		for i in range(0,len(eigenVectors)):
			weight = np.dot(img_vector, eigenVectors[i])
			t.append(weight[0])
		print(t)
		weights1 = np.asarray(weights)
		t1 = np.asarray(t)
		for i in range(0,len(weights1)):
			e = ((weights1[i] - t1)**2).mean(axis = 0)
			print(e)
		client.connect((host,port))
		client.send(bytes(str(t1), 'utf-8'))
	except Exception as e:
		print(e)
while True:
	try:
		prev_status = status
		r = requests.get(url1)
		status = r.text.split(",")[0].split(":")[2]
		print(prev_status,status)
		if(prev_status == "\"OFFLINE\"" and status == "\"ONLINE\""):
			print("MOTION DETECTED")
			camera.capture('/home/pi/Desktop/image.png')
			face_detection()
	except (KeyboardInterrupt, SystemExit):
		camera.stop_preview()
		camera.close()
		raise
	except Exception as e:
		print(e)
