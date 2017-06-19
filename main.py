from aruco import *
from perspective import *
import math
import time
import numpy as np
import cv2
import serial

from xbee import XBee
from multiprocessing import Process





#cal_dist=[]
#updated path=[]
'''
def distcheck(robot,path):
    for i in robot:
        for count,j enumerate path:
            pt1=(robot[i][0],robot[i][1])
            pt2=path[j]
            cal_dist[count][=distance(pt1,pt2)
            updated_path[i]=min(cal_dist)
'''


                            
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode
    global path
    global pathlen
    if event ==cv2.EVENT_RBUTTONDOWN:
        path=[]
    
        
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    #elif event == cv2.EVENT_MOUSEMOVE:
     #   if drawing == True:
      #      cv2.circle(img_rgb,(x,y),8,(0,0,255),-1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        
        path.append((x,y))
        cv2.circle('image',(x,y),8,(0,0,255),-1)
   
        
    #print path

#x_center=[[],[],[]]
#y_center=[[],[],[]]

def distance(pt1,pt2):
    return int(math.sqrt(((pt2[1]-pt1[1])**2)+((pt2[0]-pt1[0])**2)))

def robots(ser,botid,goal):
        global arena
        global robot
        
        i=botid
        #try:
        #    dummy=goal
        #except:
        #    'no goal'
        dummy=goal[botid]    

        
        pt1[i]=(robot[i][0],robot[i][1])
        pt2=dummy
        #print pt1[i],pt2
        cv2.circle(arena,pt2,2,(0,0,255),2)
        cv2.line(arena,pt1[i], pt2, (0,255,0))
        
        angle_i[i]=robot[i][2]
        #cv2.putText(arena,'robot'+ str(angle_i[3]),(50,70+200) ,cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)        
        ##cv2.putText(arena,'robot'+ str(angle_i[i]),(50+250*i,70) ,cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        #if angle_i<0:
        #    angle_i_s=180-angle_i
        
        #else :
        #    angle_i_s=angle_i
        
        angle_dummy[i]=angle_calculate(pt2,pt1[i])


        
        

        #if (angle_i<0 and angle_dummy>0):
        #    print'iififififi'
        #    angle_dummy=-angle_dummy
        #if (angle_i<0 and angle_dummy<0):
        #    angle_dummy=-angle_dummy
            
        angle_between[i]=int(angle_i[i]-angle_dummy[i])
        
        #if angle_between<-180:
        #    angle_between=int(angle_i+angle_dummy)
        #if angle_between>0:
        #    angle_between=int(angle_between-180)
        ##cv2.putText(arena,'dummy'+ str(angle_dummy[i]),(50+250*i,90) ,cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        ##cv2.putText(arena, 'error'+str(angle_between[i]),(50+250*i,110) ,cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        #cv2.putText(arena, 'error'+str(angle_between[3]),(50,110+70) ,cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        #if angle_between<0:
         #   angle_between=angle_between

        #print 'angledummy',angle_dummy  
        
        #print 'angle_i',angle_i
       
        
        #print'error',angle_between
       
        
        d=distance(pt1[i],pt2)
        ##cv2.putText(arena, 'distance'+str(d),(50+250*i,130) ,cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        
        #ids=str(i)
        ##x=str(robot[i][0])
        #y=str(robot[i][1])
        #theta=str(angle_i[i]+360)
        #print 'angle current', theta
        #print 'angle req', angle_between
        
        
        
        
        #print ids,x,y,theta
       ## print ('.'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(dummy[0])+'/'+str(dummy[1])+'/'+str(angle_dummy[i]+360)+'/')

        if botid==2:
            xbees.tx(dest_addr='\x00\x22',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(dummy[0])+'/'+str(dummy[1])+'/'+str(angle_dummy[i]+360)+'/#>')
        if botid==1:
            xbees.tx(dest_addr='\x00\x21',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(dummy[0])+'/'+str(dummy[1])+'/'+str(angle_dummy[i]+360)+'/#>')
        if botid==0:
           xbees.tx(dest_addr='\x00\x20',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(dummy[0])+'/'+str(dummy[1])+'/'+str(angle_dummy[i]+360)+'/#>') 
        if botid==3:
           xbees.tx(dest_addr='\x00\x23',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(dummy[0])+'/'+str(dummy[1])+'/'+str(angle_dummy[i]+360)+'/#>')
        if botid==4:
           xbees.tx(dest_addr='\x00\x24',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(dummy[0])+'/'+str(dummy[1])+'/'+str(angle_dummy[i]+360)+'/#>')
        if botid==5:
           xbees.tx(dest_addr='\x00\x25',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(dummy[0])+'/'+str(dummy[1])+'/'+str(angle_dummy[i]+360)+'/#>')

        #ser.write('?'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(dummy[0])+'/'+str(dummy[1])+'/'+str(angle_dummy+360)+'/')
        #p=ser.read()
        #print 'reading',p


try:
    ser=serial.Serial(port='COM8',baudrate=9600)
    xbees=XBee(ser)
except:
    pass
#print 'max bot id'



ix,iy = -1,-1

path=[]

angle_i=[[],[],[],[],[],[]]
angle_between=[[],[],[],[],[],[]]
angle_dummy=[[],[],[],[],[],[]]
pt1=[[],[],[],[],[],[]]
cap=cv2.VideoCapture(1)
robot={}

goal=[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
dummy=()
start_time=time.time()
time.sleep(3)


def goalallocate(path,goal):
    
    #drawing = False
    #cv2.setMouseCallback('arena',draw_circle)
    #print path
    global robo
    global img_rgb
    for botid in robot:
        dist_ance=[[],[],[],[],[],[]]
        for count,j in enumerate(path):

            #print count
            pt3=(robot[botid][0],robot[botid][1])
            pt4=j
            dist_ance[count]=distance(pt3,pt4)


            

        #print 'ddddddddddd',dist_ance
        goal_index=dist_ance.index(min(dist_ance))
        #print 'ggggggggggg',goal_index
        if (goal[botid]==(0,0)) and path!=[]:
        
            goal[botid]=path[goal_index]
          
        
            path.remove(goal[botid])
            #print 'goal',goal

def movement(path,goal):
   
        
        
    global img_rgb
    global arena
    global robot
    #img_rgb=cv2.imread('test_marker 5X50.jpg')
    
    
    
    #arena=img_rgb
    #height,width,_=arena.shape

   
    #pathlen=len(robot)

    
    goalallocate(path,goal)
    
    '''
    print 'path',path
    print 'goal',goal
    #print 'goal len',len(goal)
    cv2.imshow('arena',arena)
    cv2.imshow('Orignal video',img_rgb)
    '''

    #timestart=time.time()
    print 'path',path
    print 'goal',goal
    #print 'statr',start_time
    
    #img_rgb=cv2.imread('test_marker 5X50.jpg')
        
    #arena=img_rgb
    
    print robot
    #time_update=time.time()
    #print 'updated',time_update
    '''
    if time_update>start_time+5:
        print 'updated'
        
        
        start_time=time_update
    '''
    #print 'robot dict',robot
    
   # goalallocate(img_rgb,robot,path,goal)
    
    #print 'while',goal
    #goal is a list of pints selected on arena frame index with 0,1,2,....
    #robot is dictionay of robot id x,y,angle
    #ser is serial initalas
    #arean is arena image
    #bot id is used to
    for i in path:
        cv2.circle(arena,i,4,(0,0,255),-1)
    for i in robot:
        
        botid=i
        
        #robot=aruco_detect(arena,robot)
       
        robots(ser,botid,goal)
        
    cv2.imshow('arena',arena)
    #cv2.imshow('Orignal video',img_rgb)
   
    
    #endtime=time.time()
    #total=endtime-timestart

    #print 'total',total
   
    

while(1):
    start_time1=time.time()
    _,img_rgb=cap.read()
    arena=mainarea(img_rgb)
    robot=aruco_detect(arena,robot)
    movement(path,goal)

    
    k=cv2.waitKey(20) & 0xFF
    if k==97:
        goal=[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
        path=[(190, 284), (269, 67), (357, 285), (314, 176), (221, 177)]
    if k==35:
        import shapedraw
        path=shapedraw.path
    if k == 27:
        cv2.destroyAllWindows()
        break
    if k==121:
        goal=[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
        path=[(214, 91), (321, 200), (423, 86), (238, 315),(400,300)]
    end_time1=time.time()
    
    print 'timeeeee',(end_time1-start_time1)
