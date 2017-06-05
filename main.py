from aruco import *
from perspective import *
import math
import time
import numpy as np
import cv2
import serial

ser=serial.Serial(port='COM8',baudrate=9600)


x_center=[[],[],[]]
y_center=[[],[],[]]
angle=[[],[],[]]
cap=cv2.VideoCapture(2)
robot={}
start_time=time.time()
def distance(pt1,pt2):
    return int(math.sqrt(((pt2[1]-pt1[1])**2)+((pt2[0]-pt1[0])**2)))

def bot1(arena,ser,robot):
    
    for i in robot:

        
        
        dummy=(200,200)
        
        pt1=(robot[i][0],robot[i][1])
        pt2=(200,200)
        
        cv2.circle(arena,pt2,2,(0,0,255),2)
        cv2.line(arena,pt1, pt2, (0,255,0))
        
        angle_i=robot[i][2]
        cv2.putText(arena,'robot'+ str(angle_i),(50,70) ,cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        #if angle_i<0:
        #    angle_i_s=180-angle_i
        #else :
        #    angle_i_s=angle_i
        
        angle_dummy=angle_calculate(pt2,pt1)


        
        

        #if (angle_i<0 and angle_dummy>0):
        #    print'iififififi'
        #    angle_dummy=-angle_dummy
        #if (angle_i<0 and angle_dummy<0):
        #    angle_dummy=-angle_dummy
            
        angle_between=int(angle_i-angle_dummy)
        
        #if angle_between<-180:
        #    angle_between=int(angle_i+angle_dummy)
        #if angle_between>0:
        #    angle_between=int(angle_between-180)
        cv2.putText(arena,'dummy'+ str(angle_dummy),(50,90) ,cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        cv2.putText(arena, 'error'+str(angle_between),(50,110) ,cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        #if angle_between<0:
         #   angle_between=angle_between

        print 'angledummy',angle_dummy    
        #print 'angle_dummy',angle_dummy
        print 'angle_i',angle_i
        #error=angle_between+angle_i
        #print 'errrr',error
        print'error',angle_between
        #print'corrected angle',math.degrees(math.atan2(math.sin(),math.cos(e)))
        
        d=distance(pt1,pt2)
        cv2.putText(arena, 'distance'+str(d),(50,130) ,cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        
        ids=str(i)
        x=str(robot[i][0])
        y=str(robot[i][1])
        theta=str(angle_i+360)
        #print 'angle current', theta
        #print 'angle req', angle_between
        
        
        
        
        print ids,x,y,theta
        ser.write('.'+ids+'/'+x+'/'+y+'/'+theta+'/'+'200'+'/'+'200'+'/'+str(angle_dummy+360)+'/')
        #p=ser.read()
        #print 'reading',p

    

time.sleep(3)
while(1):
    
    #print 'statr',start_time
    _,img_rgb=cap.read()
    
    #img_rgb=cv2.imread('test_marker 5X50.jpg')
    arena=mainarea(img_rgb)    
    #arena=img_rgb
    robot=aruco_detect(arena,robot)

    time_update=time.time()
    #print 'updated',time_update
    if time_update>start_time+5:
        print 'updated'
        
        robot={}
        start_time=time_update
    print 'robot dict',robot
    
    bot1(arena,ser,robot)
    



    cv2.imshow('arena',arena)
    cv2.imshow('Orignal video',img_rgb)



    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
            
        break
