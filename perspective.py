import cv2
import numpy as np

'''
File Name:perspective
Funtions:mainarea
Global Variable:
                    
'''
'''
Function Name:mainarea
Input:frame(image from camera)
Output:back box enclosed area in image or returns the same image
Logic:contours of specific area in selected to fet the largest black box in area
Example Call:
'''
def mainarea(img_rgb):
    
    
    img_gray=cv2.cvtColor(img_rgb,cv2.COLOR_BGR2GRAY) #converts image int gray image
    ret,thresh = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY) #converts image into binary
    #cv2.imshow('thresh',thresh)
    _,contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)#find contours in the image
    
    x=0 #initial x corner of black box rectagle
    y=0 #nitial y corner of block box rectangle
    w=0 #initial width of black box rectangle
    h=0 #initial height of black box rectangle
    if contours:
        for contour in contours:
            
            #approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
            area = cv2.contourArea(contour) #calculate the area of contour detected
        
            if (area >100000)and area<250000 : # true if area is between range may vary with the height of camera set each time when camera height is changed
                

        


                
                x,y,w,h = cv2.boundingRect(contour) #gives x,y,w,h of rectangle around contour
                
                cv2.rectangle(img_rgb,(x,y),(x+w,y+h),(0,0,255),2) #draw bounding rectangle around rectangle 
                #print x,y,w,h
        if w>0 and h>0:
            
            
            crop_img = img_rgb[y:y+h, x:x+w] #crop black rectangel from the frame
            pts1 = np.float32([[x,y],[x+w,y],[x,y+h],[x+w,y+h]]) # rectangle for perspective transform
            pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]]) #canvas size for perspective transform
            M = cv2.getPerspectiveTransform(pts1,pts2) #perspective transform of the frame


            arena = cv2.warpPerspective(crop_img,M,(w,h)) #wrap perspectie
            #cv2.imshow('Arena',arena)

            
            #cv2.imshow('cropped',crop_img)
            return arena #returns image of black box arena
        else:
            
            return img_rgb #returns image of frame as it is

'''
to make the script stand alone and check persperctive transform of black box arena
decomment the below code change the comport if required
'''
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
