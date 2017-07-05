'''
File Name:main.py
Prohject:Formation control in swarm robotics
Funtions:draw_shape,draw_circle,distance,robot_comamand,goal_allocate,chunkIt,movement,drawshape
Global Variable:ix,iy,path,ser,xbees,cap,robot,goal_initial,goal,points,dummy,randompoint,randomshape
                    drawing,canavas_bool,check,img_rgb,distancemat,anglemat,obstacleavoid
                    
'''



from aruco import *
from perspective import *
import math
import time
import numpy as np
import cv2
import serial
from alphabet import * 
from xbee import XBee


'''
Function Name: draw_shape
Input: Event flag, x ,y ,flags,param
Output:Returns the x,y coordinate and appends it to points list 
Logic: these function is called by  mouse handler function
        it records all the x,y position of the mouse when button is pressed and moved in the window
Example call: cv2.setMouseCallback('canavas',draw_shape) canavas is the targeted windo

'''
def draw_shape(event,x,y,flags,param):
    global ix,iy,drawing,mode
    global canavas
    global height
    global width
    if event ==cv2.EVENT_RBUTTONDOWN: #true when mouse right button down
        canavas=np.zeros((height,width,3), np.uint8)
        
    if event == cv2.EVENT_LBUTTONDOWN: #true when left button down
        drawing = True  #flag to enable drag like event
        ix,iy = x,y

    elif  event == cv2.EVENT_MOUSEMOVE: #tru when mouse is pressed and move
        if drawing==True:
            points.append((x,y))  #add (x,y) to poits array
            cv2.circle(canavas,(x,y),5,(0,255,255),-1) #draw circle on the target window
            
    elif event == cv2.EVENT_LBUTTONUP: #true when left button released
        drawing = False
        cv2.circle(canavas,(x,y),5,(0,255,255),-1)
        points.append((x,y)) #add (x,y) to points array


'''this function is called by mouse handeler function
it appends the path list with x,y coordinate of mouse in window for every mouse down and following release. 

'''                        
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode
    global path
    global pathlen
    global points
    global arena
    
    if event ==cv2.EVENT_RBUTTONDOWN:
        path=[]
        goal=[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
    
        
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif (randomshape==True and event == cv2.EVENT_MOUSEMOVE):
        if drawing==True:
            points.append((x,y))
            cv2.circle(arena,(x,y),8,(255,255,255),-1)
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        path.append((x,y))
        cv2.circle(arena,(x,y),8,(255,255,255),-1)
   
'''
Function name:distance
Input:x,y coordinate of two points
Output:distnace between two points
Logic:This function is used to calculate the distance between two points
Example Call: distance((100,100),(200,200))
'''
def distance(pt1,pt2):

    return int(math.sqrt(((pt2[1]-pt1[1])**2)+((pt2[0]-pt1[0])**2))) #math.sqrt for square root of number



'''
Function name:robot_command
Input:serial comm. object 'ser',marker id 'botid',array of goal points'goal'
Output:Sends packets to the desired xbee
Logic:The robot_command function takes the arguments 'ser' for serial communication,'botid' i.e the id of aruco marker and the list of goal points selected.
The funtion calculates the angle between the robot and the goal point of the robot.
Xbees.tx function is used to send data packets to xbee connected serially to the PC .
Example Call:robot_command(ser,1,(200,200)) sends commaand to bot id 1 with goal location as (200,200)

'''
def robot_command(ser,botid,goal):
        global arena
        global robot
        
        i=botid
        dummy=goal[botid]    

        
        pt1=(robot[i][0],robot[i][1])
        pt2=dummy
        
        cv2.circle(arena,pt2,2,(0,0,255),2)
        cv2.line(arena,pt1, pt2, (0,255,0))
        
        angle_i=robot[i][2]
                
        angle_dummy=angle_calculate(pt2,pt1)
        
     
        if obstacleavoid==False:
            if botid==0:
               xbees.tx(dest_addr='\x00\x20',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(dummy[0])+'/'+str(dummy[1])+'/'+str(angle_dummy+360)+'/'+'0'+'0'+'/#>')
            if botid==1:
               xbees.tx(dest_addr='\x00\x21',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(dummy[0])+'/'+str(dummy[1])+'/'+str(angle_dummy+360)+'/'+'0'+'0'+'/#>')
            if botid==2:
               xbees.tx(dest_addr='\x00\x22',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(dummy[0])+'/'+str(dummy[1])+'/'+str(angle_dummy+360)+'/'+'0'+'0'+'/#>')
            if botid==3:
               xbees.tx(dest_addr='\x00\x23',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(dummy[0])+'/'+str(dummy[1])+'/'+str(angle_dummy+360)+'/'+'0'+'0'+'/#>')
            if botid==4:
               xbees.tx(dest_addr='\x00\x24',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(dummy[0])+'/'+str(dummy[1])+'/'+str(angle_dummy+360)+'/'+'0'+'0'+'/#>')
            if botid==5:
               xbees.tx(dest_addr='\x00\x25',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(dummy[0])+'/'+str(dummy[1])+'/'+str(angle_dummy+360)+'/'+'0'+'0'+'/#>')
            if botid==6:
               xbees.tx(dest_addr='\x00\x26',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(dummy[0])+'/'+str(dummy[1])+'/'+str(angle_dummy+360)+'/'+'0'+'0'+'/#>')
            if botid==7:
               xbees.tx(dest_addr='\x00\x27',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(dummy[0])+'/'+str(dummy[1])+'/'+str(angle_dummy+360)+'/'+'0'+'0'+'/#>')

      

try:
    ser=serial.Serial(port='COM8',baudrate=115200)
    xbees=XBee(ser)
except:
    pass






'''
Function Name:goalallocate
Input:path array,goal array
Output:elements in path get transferred to goal array where index is id of robot 
Logic:path is the list of raw points selected on the canavas
Goal is the list of points allocated to each robot, index of goal list denotes the id of the marker and the the data in that index is the goal point for the robot of that marker
this function iterate through the path list and the robot list and finds the shortest distance goal for each robot which is moved to respective goal indexes.
the path list becomes empty if all bots get a goal point.
Example Call:goalallocate(path,goal)

'''
def goalallocate(path,goal):
    
   
    global robot #dictionary of detected robots
    global img_rgb #image captured by the camera
    for botid in robot: #loop to iterate every id in robot dict.
        distance_list=[[],[],[],[],[],[],[],[]] #distance list initialize
        for count,j in enumerate(path): #loop to calculate distance of all oint from the robot 

            
            pt3=(robot[botid][0],robot[botid][1]) 
            pt4=j
            distance_list[count]=distance(pt3,pt4)


            

        
        goal_index=distance_list.index(min(distance_list)) #selecting minimum distance value from the distance list of 1 robot 
        
        
        if (goal[botid]==(0,0)) and path!=[]:
        
            goal[botid]=path[goal_index] #replacing goal(0,0) with a valid goal point where index of goal list represent id 
          
        
            path.remove(goal[botid]) # remove the point moved to goal array from path list
            
'''
Function Name:movement
Input:path,goal
Output:calling functions goalallocate and robot_command for every key in robot dictionary
Logic:movement function calls the function goal allocate and robot_command
robot_command is called for every element in the robot dictionary.
Example Call:movement(path,goal))
'''
def movement(path,goal):
   
    global img_rgb 
    global arena
    global robot
   

    
    goalallocate(path,goal)
   
    for i in robot: 
        
        botid=i
       
        robot_command(ser,botid,goal) #robot_command is called for every key in robot dictionary
        
    cv2.imshow('arena',arena) # show the image catured by image




'''
Function Name:chunkIt
Input:array,no of parts
Output:array split in desired no of smaller arrays
Logic:this function is used to slice the list in eight parts based on the average ,
it ensures the list is divided in parts regardless of the no of elements in each part
Example Call:chunkIt(array,8)

'''
def chunkIt(seq, num):
  avg = len(seq) / float(num)
  out = []
  last = 0.0

  while last < len(seq):
    out.append(seq[int(last):int(last + avg)])
    last += avg

  return out


'''
Function Name:drawshape
Input:8 list
Output:8 points path list
Logic:This function calls the chunkIt function which gives a list of 8 lists
The average of each list is taken and hence 8 points are obtained from 8 lists.
Example Call:

'''
def drawshape():
    #print points
    chunk=chunkIt(points,8) #big array spilt into small arrays
 

    for i in range(len(chunk)):
        #print i
        sumx=0
        sumy=0
        for j in (chunk[i]):
            #print j
            sumx=(j[0]+sumx) # sum all x values
            sumy=(j[1]+sumy) #sum all y values
        tx=sumx/len(chunk[i]) #average (sum/no of elements)
        ty=sumy/len(chunk[i])
        
        path.append((tx,ty)) # add the average point in the path list
        
        cv2.circle(arena,(tx,ty),5,(255,255,0),-1) #draw average point 
       # print sumx,sumy,tx,ty
       # print path
    return path



'''Function Name:obstacle avoid
Input:robot dictionary
Output:xbee packet to trigger robot to move left right and avoid collision
Logic:This function is used to calculate the distance and angle between robots.
Distance matrix and anglematrix is used to save the distance and angle between each robot to robot.

Also np.where function is used to regularly check if any value in the list is below the threshhold value.

if any value of distance and angle matrix is less than the defined threshhold value indicated that some another bot is approching collision.
A signal is send to the robot with flag 1 or 2  and the angle dependng on left ,right motion it should take in order to avoid collision

Example Call:obstacle avoid(robot)'''

            
def obstacle_avoid(robot):

    '''distance matrix-a distance matrix is a square matrix (two-dimensional array) containing the distances, taken pairwise, between the elements of a set.'''

    '''angle matrix-an angle matrix matrix is a square matrix (two-dimensional array) containing the angles, taken pairwise, between the elements of a set
    Here the angles are relative angles'''
    for i in robot:
        for j in robot:
            try:
                
                distancemat[i][j]=distance((robot[i][0],robot[i][1]),(robot[j][0],robot[j][1])) #distance b/w robot i and robot j
            except:
                pass
            obsy=(robot[j][1]-robot[i][1])
            obsx=(robot[j][0]-robot[i][0])
            angle_360=angle_calculate((robot[j][0],robot[j][1]),(robot[i][0],robot[i][1]))-robot[i][2] #angle b/w robot i and robot j, with respect to angle of robot i (relative angle)
            
            try:
                anglemat[i][j]=math.degrees(math.atan2(math.sin(angle_360*(math.pi/180)),math.cos(angle_360*(math.pi/180)))) #relative angle in range(-180 to 180) 
            except:
                pass
          
            try:
                item=np.where(np.logical_and(distancemat[i][j]<80,distancemat[i][j]>0))  #searching distance matrix
                an=np.where(np.logical_and(anglemat[i][j]<90 , anglemat[i][j]>-90))     #searching angle matrix
            except:
                pass
            #print i,j,len(an[0]),len(item[0])
            if (len(an[0])!=0)  and i!=j and len(item[0])!=0  : #condition for threshhold
                obstacleavoid=True
                #print 'trig',i,j,distancemat[i][j],anglemat[i][j]

                sendangle=90-abs(anglemat[i][j]) #turning angle for bot.

                '''
                send command to bot 'left' or 'right' and the angle for turning
                '''
                
                if anglemat[i][j]>0 and (i<8 or i>=0):
                    #print 'left'
                    if i==2:
                        xbees.tx(dest_addr='\x00\x22',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(0)+'/'+str(0)+'/'+str(0)+'/'+'1'+'/'+str(sendangle)+'/#>')
                    if i==1:
                        xbees.tx(dest_addr='\x00\x21',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(0)+'/'+str(0)+'/'+str(0)+'/'+'1'+'/'+str(sendangle)+'/#>')
                    if i==0:
                        xbees.tx(dest_addr='\x00\x20',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(0)+'/'+str(0)+'/'+str(0)+'/'+'1'+'/'+str(sendangle)+'/#>')
                    if i ==3:
                        xbees.tx(dest_addr='\x00\x23',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(0)+'/'+str(0)+'/'+str(0)+'/'+'1'+'/'+str(sendangle)+'/#>')
                    if i ==4:
                        xbees.tx(dest_addr='\x00\x24',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(0)+'/'+str(0)+'/'+str(0)+'/'+'1'+'/'+str(sendangle)+'/#>')
                    if i ==5:
                        xbees.tx(dest_addr='\x00\x25',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(0)+'/'+str(0)+'/'+str(0)+'/'+'1'+'/'+str(sendangle)+'/#>')
                    if i ==6:
                        xbees.tx(dest_addr='\x00\x26',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(0)+'/'+str(0)+'/'+str(0)+'/'+'1'+'/'+str(sendangle)+'/#>')
                    if i ==7:
                        xbees.tx(dest_addr='\x00\x27',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(0)+'/'+str(0)+'/'+str(0)+'/'+'1'+'/'+str(sendangle)+'/#>')




                elif anglemat[i][j]<=0 and (i<8 or i>=0):
                    #print 'right'

                    if i==2:
                        xbees.tx(dest_addr='\x00\x22',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(0)+'/'+str(0)+'/'+str(0)+'/'+'2'+'/'+str(sendangle)+'/#>')
                    if i==1:
                        xbees.tx(dest_addr='\x00\x21',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(0)+'/'+str(0)+'/'+str(0)+'/'+'2'+'/'+str(sendangle)+'/#>')
                    if i==0:
                        xbees.tx(dest_addr='\x00\x20',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(0)+'/'+str(0)+'/'+str(0)+'/'+'2'+'/'+str(sendangle)+'/#>')
                    if i ==3:
                        xbees.tx(dest_addr='\x00\x23',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(0)+'/'+str(0)+'/'+str(0)+'/'+'2'+'/'+str(sendangle)+'/#>')
                    if i ==4:
                        xbees.tx(dest_addr='\x00\x24',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(0)+'/'+str(0)+'/'+str(0)+'/'+'2'+'/'+str(sendangle)+'/#>')
                    if i ==5:
                        xbees.tx(dest_addr='\x00\x25',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(0)+'/'+str(0)+'/'+str(0)+'/'+'2'+'/'+str(sendangle)+'/#>')
                    if i ==6:
                        xbees.tx(dest_addr='\x00\x26',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(0)+'/'+str(0)+'/'+str(0)+'/'+'2'+'/'+str(sendangle)+'/#>')
                    if i ==7:
                        xbees.tx(dest_addr='\x00\x27',data='<#'+str(i)+'/'+str(robot[i][0])+'/'+str(robot[i][1])+'/'+str(robot[i][2]+360)+'/'+str(0)+'/'+str(0)+'/'+str(0)+'/'+'2'+'/'+str(sendangle)+'/#>')
            else:
                obstacleavoid=False #obstacle avoid mode off


    
                #print 'angle',j,distancemat[j][i],anglemat[j][i]
           
               # print 'angle',j,i,distancemat[i][j],anglemat[i][j]

    


    
ix,iy = -1,-1 #initail value of x,y of mouse ointer

path=[] #lsit of un alocated goal points
try: #change the comm port to the com por on which ebee is connected
    ser=serial.Serial(port='COM8',baudrate=115200) #object of serial function to enable serial communication
    xbees=XBee(ser) #objec of XBee function to enable packet generation
except:
    pass
#change the paramete to change the camera
cap=cv2.VideoCapture(2) #object to enable image read from camera and open com port of camera
robot={} #initialize dictionary
goal_initial=[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)] # initial goal point for robot
goal=goal_initial
points=[] # list to save raw points made on canvas
start_time=time.time()

randompoint=False #random point mode off 
randomshape=False #random shape off
drawing=False #drawing mode off
canavas_bool=False #canavas enable off


check,img_rgb=cap.read() # read image from camera
distancemat=np.zeros((8,8),dtype=int) #8*8 distance matrix with all element zero
anglemat=np.zeros((8,8),dtype=int) #8*8 angle matrix with all element zero
obstacleavoid=False #obstacle avoid mode off
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output2.avi',fourcc, 20.0, (640,480))



'''
this funtion checks if there is a video or not on the sepicified COM port
It gives and error and ask for COM port if video is not detected.
'''
while check!=True:   
    print 'error video not found' #error msg when video feed not found
    camport=input('Enter cam port number (0,1,2....') #ask for comport number
    cap=cv2.VideoCapture(camport) 
    check,img_rgb=cap.read()
    
'''
this while loop is used captur video from the camera and call all the functions at eevery frame refresh

'''
while(1):
    
    if canavas_bool==True: #creates a black canavas and enables mouse clicks to draw shapes and record point
        cv2.imshow('canavas',canavas) # show canavas
        cv2.setMouseCallback('canavas',draw_shape)  #Sets mouse handler for the specified window
            
    if randompoint==True or randomshape==True: #enable point by point selection of goal
        cv2.setMouseCallback('arena',draw_circle) #calls draw_circle on window arrena
        
    start_time1=time.time()   # record the time at which the statement is called
    _,img_rgb=cap.read()  # read frame from  the camera
    arena=mainarea(img_rgb)  #calls main arena function in perpective.py 'arena' is image matrix of black box area in camera image
    
    robot=aruco_detect(arena,robot) #calls function aruco_detect in aruco.py gives a dictionary'robot' ontaining id of marker as key and location and orientaion as element
    
    obstacle_avoid(robot) # calls obstacle avoid function to check distance matrix and angle matrix 
    movement(path,goal)  # calls movement function when calls goalallocate and robot_command to send xbee packets to the bot to move
    
 
    height,width,_=arena.shape #height and width of the arena image

        
    k=cv2.waitKey(20) & 0xFF # keyboard trigger also kind of delayS

    goal,path=character(k,goal,path) #calls the character function in alphabet.py to allocate path matrix and goal matrix

  
    if k==47:#/ random points
        goal=[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)] # set all goals to (0,0) stops all robots
        path=[] 
        randompoint=True # enable randompoint mode
        randomshape=False #disable drawshape mode
   
    if k==33 :#! initialize canvas
        canavas_bool=True #enable canvas
        canavas=np.zeros((height,width,3), np.uint8) # creaets a canavas 
    if k==35:#, execute shape draw
        randomshape=False
        randompoint=False
        path=[]
        goal=[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
        path=drawshape()
        points=[]
        
    if k == 27:#esc stops script
        goal=[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
        robot=aruco_detect(arena,robot)
        movement(path,goal)
        cv2.destroyAllWindows()# DESTROYE ALL windows
        break
    


        
   

    print 'timeeeee',(time.time()-start_time1) #gives time take by 1 iteration of the loop 
