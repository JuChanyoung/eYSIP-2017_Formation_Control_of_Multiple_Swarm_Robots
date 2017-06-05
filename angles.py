import cv2
import numpy as np
import math


height=200
width=200
def angle(pt1,pt2):

    
    x=pt2[0]-pt1[0]
    y=pt2[1]-pt1[1]    
    angle=math.degrees(math.atan2(y,x))

    return angle

pt1=(30,20)
pt2=(30,40)
print 'angle',angle(pt1,pt2)



    

img = np.zeros((height,width,3), np.uint8)
img[:]=(255,255,0)



#cv2.circle(img,(x1,y1),5,(0,255,255),-1)
#cv2.circle(img,(x2,y2),5,(0,0,255),-1)


cv2.imshow('image',img)
cv2.waitKey(1)
