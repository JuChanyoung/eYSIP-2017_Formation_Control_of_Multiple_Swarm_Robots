import cv2
import numpy as np

#img_rgb = cv2.imread('img.jpg')
#img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)
#img_gray=cv2.cvtColor(img_rgb,cv2.COLOR_BGR2GRAY)
#rows,cols,ch = img_rgb.shape
#print "ROWS",rows
#print "COLS",cols

def mainarea(img_rgb):
    
    
    img_gray=cv2.cvtColor(img_rgb,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)
    cv2.imshow('thresh',thresh)
    _,contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    x=0
    y=0
    w=0
    h=0
    if contours:
        for contour in contours:
            
            approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
            area = cv2.contourArea(contour)
        
            if (area >100000)and area<250000 :
                

        
       # for cnt in obstacle_list:

                
                x,y,w,h = cv2.boundingRect(contour)
                
                cv2.rectangle(img_rgb,(x,y),(x+w,y+h),(0,0,255),2)
        if w>0 and h>0:
            
            

            pts1 = np.float32([[x,y],[x+w,y],[x,y+h],[x+w,y+h]])
            pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
            M = cv2.getPerspectiveTransform(pts1,pts2)


            arena = cv2.warpPerspective(img_rgb,M,(600,400))
            #cv2.imshow('Arena',arena)

            
            
            return arena
        else:
            
            return img_rgb


'''
cap=cv2.VideoCapture(2)

while(1):
    
    _,img_rgb=cap.read()
    img_gray=cv2.cvtColor(img_rgb,cv2.COLOR_BGR2GRAY)
    mainarea(img_gray)






    #cv2.imshow('Gray',img_gray)

    rows,cols,ch = img_rgb.shape

    cv2.imshow('image',img_rgb)


    
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        
        break
    
'''
