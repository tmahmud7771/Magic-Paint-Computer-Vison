import cv2 as cv 
import numpy as np 

#Capture
cap = cv.VideoCapture(0)

#gird method
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv.cvtColor( imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


myColors = [["orange",0,100,53,56,255,255,(0,0,255)], #orange [0] =name 1:4 => h_min-s_min-v_min 4:7 => h_max-s_max-v_max
            ["blue",39,119,0,179,255,255,(255,165,0)],    
            ["green",24,48,0,107,113,95,(0,128,0)]] 


#find colors method
def findColors(img,myColors):
    imgHSV = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    for c in myColors:
        lower = np.array(c[1:4])  #lower range values array
        upper = np.array(c[4:7])  #Upper range values array
        mask = cv.inRange(imgHSV,lower,upper) #mask photo b&ws
        # cv.imshow((c[0]),mask)
        x,y = getContours(mask)
        cv.circle(imgResult,(x,y),8,c[7],cv.FILLED)

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

while True:
    isTrue, img = cap.read()
    imgResult = img.copy()
    findColors(img,myColors)
    cv.imshow("Display", imgResult)
    if cv.waitKey(1) & 0xFF == ord('f'):
        break

