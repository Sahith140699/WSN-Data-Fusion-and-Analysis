#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2  
 
face_cascade = cv2.CascadeClassifier('C:/Users/Sahith/Anaconda3/pkgs/libopencv-3.4.1-h875b8b8_3/Library/etc/haarcascades/haarcascade_frontalface_default.xml') 

#eye_cascade = cv2.CascadeClassifier('C:/Users/Sahith/Anaconda3/pkgs/libopencv-3.4.1-h875b8b8_3/Library/etc/haarcascades/haarcascade_eye.xml')  
  
    
img = cv2.imread('C:/Users/Sahith/Desktop/Internship/test.png',1)
faces = face_cascade.detectMultiScale(img, 1.3, 5)
  
for (x,y,w,h) in faces: 
    print(x,y,w,h)
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)   
    roi_color = img[y:y+h, x:x+w]
cv2.imshow('img',img)
cv2.imshow('img_face',roi_color)
img_res = cv2.resize(roi_color,(100,100),cv2.INTER_LINEAR)
# if(w < 196 and h < 196):
#     img_res = cv2.resize(roi_color,(196,196),cv2.INTER_LINEAR)
# if(w > 196, h > 196):
#     img_res = cv2.resize(roi_color,(196,196),cv2.INTER_AREA)
cv2.imwrite('C:/Users/Sahith/Desktop/Internship/a3_100.png',img_res)
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[ ]:




