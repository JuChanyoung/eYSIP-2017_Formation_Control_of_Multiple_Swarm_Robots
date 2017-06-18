import cv2
import numpy as np
from perspective import *

height=480
width=640
a=input()

cap=cv2.VideoCapture(1)
_,img_rgb=cap.read()
    




def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            points.append((x,y))
            cv2.circle(img,(x,y),5,(0,0,255),-1)
            

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        points.append((x,y))
        print path
        cv2.circle(img,(x,y),5,(0,0,255),-1)
        





path=[]
points=[]
ls=0
ss=1000
ld=0
sd=-1000
l_diff=(100,100)
for i in range(1,100):

    img=mainarea(img_rgb)

while(1):
    
    
   
    k = cv2.waitKey(20) & 0xFF

    if k==114:
        cv2.setMouseCallback('image',draw_circle)
    
        print path
    if k==115:
        for i in points:
            ts=i[0]+i[1]
            
            if ts>ls:
                ls=ts
                l_sum=i
                
            if ts<ss:
                ss=ts
                s_sum=i

            td=i[0]-i[1]

            if td<ld:
                ld=td
                l_diff=i
                
            if td>sd:
                sd=td
                s_diff=i


            
                print l_sum,s_sum
                print ls
        cv2.circle(img,(l_sum),5,(0,255,255),-1)
        cv2.circle(img,(s_sum),5,(255,0,255),-1)
        cv2.circle(img,(l_diff),5,(255,0,0),-1)
        cv2.circle(img,(s_diff),5,(0,255,0),-1)
        path=[l_sum,s_sum,l_diff,s_diff]

    if k==99:
        img = np.zeros((height,width,3), np.uint8)
        points=[]
        ls=0
        ss=1000
        ld=0
        sd=-1000

    
    if k == 27:
        cap.release()
        cv2.destroyAllWindows()
        break
    cv2.imshow('image',img)
