import numpy as np
import cv2
import cv2.aruco as aruco
import math
import datetime
import time

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
            x_center[marker]= (corners[marker][0][0][0] + corners[marker][0][1][0] + corners[marker][0][2][0] + corners[marker][0][3][0])/4
            y_center[marker] = (corners[marker][0][0][1] + corners[marker][0][1][1] + corners[marker][0][2][1] + corners[marker][0][3][1])/4
            #print(x_center,y_center)

            #print (corners[0][0][0][0], corners[0][0][0][1])
            #print (corners[0][0][1][0], corners[0][0][1][1])

            x1 = corners[marker][0][0][0]
            x2 = corners[marker][0][1][0]
            y1 = corners[marker][0][0][1]
            y2 = corners[marker][0][1][1]

            x2 = x2-x1
            y2 = -(y2-y1)

            x1=0
            y1=0

            #angle = -math.degrees(math.atan((corners[0][0][1][1] - corners[0][0][0][1])/(corners[0][0][1][0] - corners[0][0][0][0])))
            angle[marker] = math.degrees(math.atan(y2/x2))

            if angle[marker]<0:
                angle[marker] = -angle[marker]

            #print x2,y2

            if x2>0 and y2>0:
                angle[marker] = angle[marker]
            elif x2<0 and y2>0:
                angle[marker] = 180 - angle[marker]
            elif x2 < 0 and y2 < 0:
                angle[marker] = 180 + angle[marker]
            elif x2 > 0 and y2 < 0:
                angle[marker] = 360 - angle[marker]
            angle[marker]=angle[marker]-180
            #print angle
    
        #for bot in len(ids):
    
    
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
