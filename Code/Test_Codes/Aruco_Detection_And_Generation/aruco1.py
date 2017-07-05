import numpy as np
import cv2
import cv2.aruco as aruco
import math

cap = cv2.VideoCapture(0)

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
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

    if len(corners)>0:

        #print(corners)
        #print(ids)
        x_center = (corners[0][0][0][0] + corners[0][0][1][0] + corners[0][0][2][0] + corners[0][0][3][0])/4
        y_center = (corners[0][0][0][1] + corners[0][0][1][1] + corners[0][0][2][1] + corners[0][0][3][1])/4

        #print (corners[0][0][0][0], corners[0][0][0][1])
        #print (corners[0][0][1][0], corners[0][0][1][1])

        x1 = corners[0][0][0][0]
        x2 = corners[0][0][1][0]
        y1 = corners[0][0][0][1]
        y2 = corners[0][0][1][1]

        x2 = x2-x1
        y2 = -(y2-y1)

        angle = math.degrees(math.atan2(y2,x2)) #Result ranges from -180 to 180

        print angle, (x_center,y_center)
        #print(x_center,y_center)

    gray = aruco.drawDetectedMarkers(gray, corners)

    # Display the resulting frame
    cv2.imshow('frame', gray)

    #Stop if 'Q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()