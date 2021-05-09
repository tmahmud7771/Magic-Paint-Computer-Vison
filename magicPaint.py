import cv2 as cv 
import numpy as np 

#Capture
cap = cv.VideoCapture(0)
cap.set(3,1200)
cap.set(4,1000)


while True:
    isTrue, img = cap.read()
    
    cv.imshow("Display", img)

    if cv.waitKey(1) & 0xFF == ord('f'):
        break

