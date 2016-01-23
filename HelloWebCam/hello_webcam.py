import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    lower_red = np.array([0,75,75])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170,75,75])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    mask = mask0 + mask1

    mask = cv2.dilate(
        cv2.erode(mask,np.ones((5,5),np.uint8), iterations = 1),
        np.ones((5,5),np.uint8),iterations = 1)
    edges = cv2.Canny(mask, 50, 150, apertureSize = 3)

    edges = cv2.dilate(edges,np.ones((2,2),np.uint8), iterations = 1)

    # Bitwise-AND mask and original image
    # reds = cv2.bitwise_and(frame,frame, mask= mask)
    

    minLineLength = 100
    maxLineGap = 50
    lines = cv2.HoughLinesP(
        edges,
        1,
        np.pi/180,
        100,
        minLineLength,
        maxLineGap)
    if lines == None:
        lines = [[]]
    for line in lines:
        for x1,y1,x2,y2  in line:
            cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
    
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('edges',edges)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()