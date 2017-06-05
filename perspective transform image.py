import cv2
import numpy as np

img_rgb = cv2.imread('img.jpg')
img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)
img_gray=cv2.cvtColor(img_rgb,cv2.COLOR_BGR2GRAY)
rows,cols,ch = img_rgb.shape
print "ROWS",rows
print "COLS",cols

def mainarea(img_gray):
    ret,thresh = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)
    cv2.imshow('thresh',thresh)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    
    for contour in contours:
        
        approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
        area = cv2.contourArea(contour)
    
        if (area >100000)and area<250000 :
            

    
   # for cnt in obstacle_list:

            
            x,y,w,h = cv2.boundingRect(contour)
        
            cv2.rectangle(img_rgb,(x,y),(x+w,y+h),(0,0,255),2)

    x,y,w,h
    print x,y,w,h

    pts1 = np.float32([[x,y],[x+w,y],[x,y+h],[x+w,y+h]])
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    M = cv2.getPerspectiveTransform(pts1,pts2)


    dst = cv2.warpPerspective(img_rgb,M,(w,h))
    cv2.imshow('dst',dst)

    cv2.imshow('M',M)
    
    return x,y,w,h

def aruco(img_gray):
    ret,thresh = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)
    cv2.imshow('thresh',thresh)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    
    for contour in contours:
        
        approx = cv2.approxPolyDP(contours[2],0.01*cv2.arcLength(contours[2],True),True)
        area = cv2.contourArea(contour)

        #image_crop=img_gray[approx[0,0,1]:approx[2,0,1],approx[0,0,0]:approx[2,0,0]]


        cv2.drawContours(img_rgb, approx, -1, (0, 255, 0), 3)
        cv2.imshow('crop',img_rgb)
        if (area >2500)and area<5000:
            

    
   # for cnt in obstacle_list:

        
            x,y,w,h = cv2.boundingRect(contour)
        
            cv2.rectangle(img_rgb,(x,y),(x+w,y+h),(0,0,255),2)

    x,y,w,h
    print x,y,w,h

    pts1 = np.float32([[x,y],[x+w,y],[x,y+h],[x+w,y+h]])
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    M = cv2.getPerspectiveTransform(pts1,pts2)


    dst = cv2.warpPerspective(img_rgb,M,(w,h))
    cv2.imshow('dst',dst)

    cv2.imshow('M',M)
    
    return x,y,w,h



aruco(img_gray)
mainarea(img_gray)






cv2.imshow('Gray',img_gray)

rows,cols,ch = img_rgb.shape

cv2.imshow('image',img_rgb)


cv2.waitKey(0)
cv2.destroyAllWindows()

