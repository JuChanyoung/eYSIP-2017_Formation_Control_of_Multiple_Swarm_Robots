import numpy as np
import cv2
import cv2.aruco as aruco
import math
import datetime
import time



def angle_calculate(pt1,pt2):

    
    x=pt2[0]-pt1[0]
    y=pt2[1]-pt1[1]    
    angle=math.degrees(math.atan2(y,x))

    return int(angle)


#cap = cv2.VideoCapture(1)
def aruco_detect(frame,robot):
    print 'aruco_detect'
    x_center=[[],[],[]]
    y_center=[[],[],[]]
    angle=[[],[],[]]
    #robot={}
    
    #print 'start time',start
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
    parameters = aruco.DetectorParameters_create()

    #print(parameters)

    '''    detectMarkers(...)
        detectMarkers(image, dictionary[, corners[, ids[, parameters[, rejectedI
        mgPoints]]]]) -> corners, ids, rejectedImgPoints
        '''
    # lists of ids and the corners beloning to each id
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    aruco_frame = aruco.drawDetectedMarkers(gray, corners)
    cv2.imshow('aruco_frame',aruco_frame)
    print len(corners)

    if len(corners)>0:
        for marker in range(len(ids)):
            
            #print len(corners)
            #print(ids)
            x_center[marker]= int((corners[marker][0][0][0] + corners[marker][0][1][0] + corners[marker][0][2][0] + corners[marker][0][3][0])/4)
            y_center[marker] = int((corners[marker][0][0][1] + corners[marker][0][1][1] + corners[marker][0][2][1] + corners[marker][0][3][1])/4)
            #print(x_center,y_center)

            

            #print (corners[0][0][0][0], corners[0][0][0][1])
            #print (corners[0][0][1][0], corners[0][0][1][1])
            
            x1 = int(corners[marker][0][0][0])
            x3 = int(corners[marker][0][3][0])
            y1 = int(corners[marker][0][0][1])
            y3 = int(corners[marker][0][3][1])

            #x2 = x3-x1
            #y2 = -(y3-y1)

            #x1=0
            #y1=0

            #angle = -math.degrees(math.atan((corners[0][0][1][1] - corners[0][0][0][1])/(corners[0][0][1][0] - corners[0][0][0][0])))

            #pt1=(x_center[marker],y_center[marker])
            pt1=(x3,y3)
            pt2=(x1,y1)
            cv2.circle(frame,pt1,2,(0,0,255),2)
            cv2.circle(frame,pt2,2,(0,0,255),2)

            angle[marker] = angle_calculate(pt1,pt2)
            print'newww',angle[marker]
            '''
                if angle[marker]<0:
                angle[marker] = -angle[marker]

            #print x2,y2

            if x2>0 and y2>0: #I quad
                angle[marker] = angle[marker]
            elif x2<0 and y2>0: # II quad
                angle[marker] = 180 - angle[marker]
            elif x2 <= 0 and y2 < 0: #III quad
                angle[marker] = 180 + angle[marker]
            elif x2 > 0 and y2 < 0: #IV quad
                angle[marker] = 360 - angle[marker]
           # angle[marker]=angle[marker]-180
            #print angle
            
        #for bot in len(ids):
                '''
    
    if ids!=None:
        
        for markers in range(len(ids)):
            
            robot[int(ids[marker])]=(int(x_center[marker]),int(y_center[marker]),int(angle[marker]))


    #start_time_update=time.time()
    #print 'start time update',start_time_update
    #if start_time_update>start+10:
     #   robot={}
      #  start=start_time_update
       # return robot,start
        
    
    
    return robot

'''
while (True):
    
    #print 'start',start
    # Capture frame-by-frame
    ret, frame = cap.read()
    start_time_update=time.time()
    #print(frame.shape) #480x640
    # Our operations on the frame come here
    #print time.time()-start_time_update

    robot=aruco_detect(frame)
    
    print robot
           
    
    
    # Display the resulting frame
    cv2.imshow('frame',frame)
    
    #Stop if 'Q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
'''
