import cv2 as cv 
import numpy as np 

#Capture
cap = cv.VideoCapture(0)

myColors = [[0,100,53,56,255,255], #orange [0] =name 1:4 => h_min-s_min-v_min 4:7 => h_max-s_max-v_max [7] = pointer color
            [39,119,0,179,255,255],    
            [24,48,0,107,113,95]]

ColorCode  = [[255,165,0],[0,0,255],[0,128,0]] #orange blue green

myPoints = []  #x,y,colorindex


#find colors method
def findColors(img,myColors,pointColor):
    imgHSV = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    counter = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])  #lower range values array
        upper = np.array(color[3:6])  #Upper range values array
        mask = cv.inRange(imgHSV,lower,upper) #mask photo b&ws
        x,y = getContours(mask)
        cv.circle(imgResult,(x,y),8,pointColor[counter],cv.FILLED)
        if x!=0 and y != 0:
            newPoints.append([x,y,counter])
        counter +=1
    return newPoints

#Contoures method

def getContours(img):
    contours,hierarchy = cv.findContours(img,cv.RETR_EXTERNAL,
    cv.CHAIN_APPROX_NONE) #rete_ex is for fining the outer part of shape
    x, y, w, h = 0,0,0,0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 500: #we will detect shape avobe 500 area , in this we can we won't detect nosied area
            # cv.drawContours(imgResult,cnt,-1,(255,0,255),3)
            param = cv.arcLength(cnt,True)  
            aprox = cv.approxPolyDP(cnt,0.02*param,True) #its a array .inside this array we have all the individual corner values  
            x, y, w, h = cv.boundingRect(aprox) #it will help to create a box aroud the shape for detect the shape it has 4 values
    return x+w//2 , y


def drawOnCanvas(recntPoints,pointColor):
    for point in recntPoints:
        cv.circle(imgResult,(point[0],point[1]),8,pointColor[point[2]],cv.FILLED)



while True:
    isTrue, img = cap.read()
    imgResult = img.copy()
    newPoints = findColors(img,myColors,ColorCode)
    if len(newPoints) !=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,ColorCode)
    
    cv.imshow("Display", imgResult)
    if cv.waitKey(1) & 0xFF == ord('f'):
        break

