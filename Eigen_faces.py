import cv2
import numpy as np
import time
import os
import sys
from sklearn.metrics import mean_squared_error

path = "C:/Users/Sahith/Desktop/Internship/images/"


##Preparation of Data
images = []

for i in os.listdir('C:/Users/Sahith/Desktop/Internship/images/'):
    im = cv2.imread(path + i, 1)
    im = np.float32(im)/255
    images.append(im)
    imFlip = cv2.flip(im,1)
    images.append(imFlip)

numImages = len(images)
sz = images[0].shape
data = np.zeros((numImages, sz[0]*sz[1]*sz[2]), dtype=np.float32)
for i in range(0,numImages):
    image = images[i].flatten()
    data[i,:] =  image

NUM_EIGEN_FACES = 10
MAX_SLIDER_VALUE = 255


##PCA

print("Calculating PCA ", end="...")
mean, eigenVectors = cv2.PCACompute(data, mean=None, maxComponents=NUM_EIGEN_FACES)
print ("DONE")
averageFace = mean.reshape(sz)


##Calculation of eigenFaces
eigenFaces = []; 

for eigenVector in eigenVectors:
    eigenFace = eigenVector.reshape(sz)
    eigenFaces.append(eigenFace)
    out = cv2.resize(eigenFace, (0,0), fx=2, fy=2)
    cv2.imshow("output",out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
cv2.namedWindow("Result", cv2.WINDOW_AUTOSIZE)

output = cv2.resize(averageFace, (0,0), fx=2, fy=2)
cv2.imshow("Result", output)
cv2.waitKey(0)
cv2.destroyAllWindows()

##Calculation of Weights
weights = []

for i in os.listdir('C:/Users/Sahith/Desktop/Internship/images/'):
    print(i)
    im = cv2.imread(path + i, 1)
    im = np.float32(im)/255
    imVector = im.flatten() - mean
    output = averageFace
    temp = []
    for i in range(0,len(eigenVectors)):
        weight = np.dot(imVector, eigenVectors[i])
        temp.append(weight[0])
    print(temp)
    weights.append(temp)
        


img = cv2.imread('C:/Users/Sahith/Desktop/Internship/test_100.png',1)
img = np.float32(img)/255.0
imgVector = img.flatten() - mean
print("Done")

output = averageFace

t = []
for i in range(0,len(eigenVectors)):
    weight = np.dot(imgVector, eigenVectors[i])
    t.append(weight[0])
    print(weight)
    output = output + eigenFaces[i] * weight
cv2.imshow("result", output)

cv2.waitKey(0)
cv2.destroyAllWindows()
     
##Calculation errors

for i in range(0,len(weights)):
    e = mean_squared_error(t,weights[i])
    print(e)


