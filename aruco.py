import numpy as np
import cv2
import cv2.aruco as aruco
import math
import datetime
import time

'''
File Name:aruco
Funtions:angle_calculate,sruco_detect
Global Variable:
                    
'''
'''
Function Name:angle_calculate
Input: 2 point in tuple format
Output: angle in range(-180,180)
Logic:math.atan2 is used to ensure range
Example Call:
'''
def angle_calculate(pt1,pt2):

    
    x=pt2[0]-pt1[0] # unpacking tuple
    y=pt2[1]-pt1[1]    
    angle=math.degrees(math.atan2(y,x)) #takes 2 points nad give angle with respect to horizontal axis in range(-180,180)

    return int(angle)



'''
Function Name:
Input:
Output:
Logic:
Example Call:
'''
def aruco_detect(frame,robot):

    #print 'start time',start
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert frame into gray image
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250) # threshold image i.e converts igray image in binary imaeg
    parameters = aruco.DetectorParameters_create() # set predefined parameretr for aruco detection
    
    # lists of ids and the corners beloning to each id
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    

    aruco_frame = aruco.drawDetectedMarkers(gray, corners) # drwa boundary of detected markers
    #cv2.imshow('aruco_frame',aruco_frame)
    #print len(corners)
    #print corners
    if len(corners)>0:
        
        for marker in range(len(ids)):
            
            #print len(corners)
            #print(ids)
            #calculate center point of the marker
            x_center= int((corners[marker][0][0][0] + corners[marker][0][1][0] + corners[marker][0][2][0] + corners[marker][0][3][0])/4)
            y_center= int((corners[marker][0][0][1] + corners[marker][0][1][1] + corners[marker][0][2][1] + corners[marker][0][3][1])/4)
            #print(x_center,y_center)

    
            cv2.circle(frame,(x_center,y_center),2,(0,0,255),2) #draw center point of the marker
            x1 = int(corners[marker][0][0][0]) #x of corner1
            x3 = int(corners[marker][0][3][0]) #x of corner3
            y1 = int(corners[marker][0][0][1]) #y of corner1
            y3 = int(corners[marker][0][3][1]) #y of corner3

            '''corner1_____________corner 3
                        | aruco     |
                        | marker    |
                        |           |
                corner 2|___________|corner 4
                
            '''
            pt1=(x3,y3)
            pt2=(x1,y1)
            cv2.circle(frame,pt1,2,(0,0,255),2) # draw corner 1
            cv2.circle(frame,pt2,2,(0,0,255),2) #drwa corner 3

            angle = angle_calculate(pt1,pt2) # calculate angle of robot in range(-180,180)
            #print'newww',angle[marker]
            
            robot[int(ids[marker])]=(int(x_center),int(y_center),int(angle)) #robot dictionary


    #start_time_update=time.time()
    #print 'start time update',start_time_update
    #if start_time_update>start+10:
     #   robot={}
      #  start=start_time_update
       # return robot,start
        
    
    
    return robot
'''
to make a stand alone script and test the aruco detection
de-comment the below'''
'''

robot={}
cap=cv2.VideoCapture(1) #chaneg com port if required
while(1):
     _,img_rgb=cap.read()

     robot=aruco_detect(img_rgb,robot)
     
     cv2.imshow('Orignal video',img_rgb)
     k = cv2.waitKey(1) & 0xFF
     if k == 27:
         cap.release()
         cv2.destroyAllWindows()
         break


'''

