wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 7

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

import numpy as np
import cv2
import os
from PIL import Image, ImageDraw
import math 
import time
import handTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

# Get default audio device using PyCAW
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# Get current volume 
currentVolumeDb = volume.GetMasterVolumeLevel()
     
 
wcam,hcam=640,480
cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
pTime=0
detector = htm.handDetector(detectionCon=0.75)

LastPx = 800
LastPy = 0

Percent = 0

while True:
    # Background = Image.open('Background.jpg')
    success,img=cap.read()
    
    img = detector.findHands(img, draw=True )
    lmList=detector.findPosition(img,draw=False)
    #print(lmList)
    tipId=[4,8,12,16,20]

    #Rectangle

    if(len(lmList)!=0):
        fingers=[]
        #thumb
        if(lmList[tipId[0]][1]>lmList[tipId[0]-1][1]):
                fingers.append(1)
        else :
                fingers.append(0)
        #4 fingers
        for id in range(1,len(tipId)):
            
            if(lmList[tipId[id]][2]<lmList[tipId[id]-2][2]):
                fingers.append(1)
            
            else :
                fingers.append(0)
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:] #2nd finger
            # x0, y0 = lmList[12][1:] #Middle Finder
            x0, y0 = lmList[4][1:]  #thumb

        # print(f'1{fingers[0]}')
        # print(f'2{fingers[1]}')
        # print(f'3{fingers[2]}')
        # print(f'4{fingers[3]}')
        # print(f'5{fingers[4]}')

        # if fingers[1] == 1 and fingers[2] == 0:  #for 2nd finger and al finger close
        if fingers[1] == 1 and fingers[0] == 1:
            #2nd Finger
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, 1080))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, 720))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
        
            cv2.circle(img, (x1, y1), 15, (0, 0,255), cv2.FILLED)
            plocX, plocY = clocX, clocY 

            #THUMB
            x3 = np.interp(x0, (frameR, wCam - frameR), (0, 1080))
            y3 = np.interp(y0, (frameR, hCam - frameR), (0, 720))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
        
            cv2.circle(img, (x0, y0), 15, (0, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

            cv2.line(img,(x1,y1),(x0,y0),(0,0,255),2)
            distance = math.sqrt((x1-x0)*(x1-x0)+(y1-y0)*(y1-y0))
            # print(distance)


            if distance<50:
                distance = 50
            elif distance>250:
                distance=250
            Percent = round((distance-50.0)/2)
            # print(Percent)
                
                
    # Changevolume = round(0.6525*math.log(Percent/100)*100)
    Changevolume = round(math.log((Percent/10)+1)*50*0.54 )
    print(Changevolume)
    volume.SetMasterVolumeLevel(-65.25+Changevolume, None)



    height = int(340 - (Percent*2.0))
    print(height)
    cv2.rectangle(img,(570,height),(620,340),(0,255,0),-1)
    cv2.rectangle(img,(570,140),(620,340),(255,0,0),2)
    img = cv2.flip(img, 1)
            
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (15,130)
    fontScale              = 1
    fontColor              = (0,0,0)
    lineType               = 2

    cv2.putText(img,f'{Percent}%', bottomLeftCornerOfText, font, fontScale,fontColor,lineType)
    
    cTime=time.time()
    fps=1.0/float(cTime-pTime)
    pTime=cTime
    
    cv2.imshow("image",img)
    


    # Background = cv2.imread('Background.jpg')
    # Background = cv2.flip(Background, 1)
    # cv2.imshow('img',Background)


    if(cv2.waitKey(1) & 0xFF== ord('q')):
        break


cap.release()

cv2.destroyAllWindows()
