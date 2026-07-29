import cv2
import numpy as np
import time
import os
import handtrackingModule as htm

folderPath="Headers"
myList=os.listdir(folderPath)
overlayList=[]



for impath in myList:
    image=cv2.imread(f'{folderPath}/{impath}')
    overlayList.append(image)

header=overlayList[0]

drawColor=(255,0,255)
xp=0
yp=0
brushThickness=15
imgCanvas=np.zeros((720,1280,3),np.uint8)

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector=htm.handDetector(detectionCon=0.85)

while True:
    success,img=cap.read()
    img=cv2.flip(img,1)

    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        # print(lmList)

        #tip of index finger
        x1,y1=lmList[8][1:]
        #tip of middle finger
        x2,y2=lmList[12][1:]

        #checking which fingers are up
        fingers=detector.fingersUp()
        # print(fingers)

        #selection mode:if 2 fingers up
        if fingers[0] and fingers[1]:
            xp,yp=0,0
            if y1<125:
                if 190<x1<330:
                    drawColor=(255,0,0)
                elif 380<x1<520:
                    drawColor=(0,0,255)
                elif 560<x1<700:
                    drawColor=(0,255,0)
                elif 910<x1<1050:
                    drawColor=(0,0,0)
            cv2.rectangle(img,(x1,y1-35),(x2,y2+35),drawColor,cv2.FILLED)
        # paint mode:if 1 finger up
        if fingers[0] and fingers[1]==False:
            cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
            if xp==0 and yp==0:
                xp,yp=x1,y1
            if drawColor==(0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,50)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,50)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)
            xp,yp=x1,y1
            





    img[0:125,0:1280]=header
    img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0)



    cv2.imshow("Image",img)
    # cv2.imshow("Canvas",imgCanvas)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()

