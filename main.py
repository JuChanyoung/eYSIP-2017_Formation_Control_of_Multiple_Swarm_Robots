from aruco import *
from perspective import *
import math
import time
import numpy as np
import cv2

x_center=[[],[],[]]
y_center=[[],[],[]]
angle=[[],[],[]]
cap=cv2.VideoCapture(2)
robot={}
start_time=time.time()
print cap
while(1):
    print 'statr',start_time
    _,img_rgb=cap.read()
    
    arena=mainarea(img_rgb)    
    
    robot=aruco_detect(arena,robot)

    time_update=time.time()
    print 'updated',time_update
    if time_update>start_time+5:
        print 'updated'
        time.sleep(.5)
        robot={}
        start_time=time_update
    print 'robot dict',robot

    cv2.imshow('arena',arena)
    cv2.imshow('Orignal video',img_rgb)



    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
            
        break
