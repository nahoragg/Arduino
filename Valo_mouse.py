import cv2
import os
from mss import mss
import numpy as np
import win32api
import serial

fov = int(input("FOV: "))
sct = mss()
 
 
arduino = serial.Serial('COM6', 115200)
 
screenshot = sct.monitors[1]
screenshot['left'] = int((screenshot['width'] / 2) - (fov / 2))
screenshot['top'] = int((screenshot['height'] / 2) - (fov / 2))
screenshot['width'] = fov
screenshot['height'] = fov
center = fov/2

lower_color = np.array([140,111,160])
upper_color = np.array([148,154,194])

speed = float(input("SPEED: "))
 
def mousemove(x):
     #Convert the values to unsigned integers
    if x < 0: 
        x = x+256 
    if y < 0:
        y = y+256 
 
    coord = [int(x),int(y)]
    arduino.write(coord)
 
 
while True:
    if win32api.GetAsyncKeyState(0x01) < 0:
        
        img = np.array(sct.grab(screenshot))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #convert
        mask = cv2.inRange(hsv, lower_color,upper_color) #color mask
        kernel = np.ones((3,3), np.uint8)
        dilated = cv2.dilate(mask,kernel,iterations=5)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1] #binary image
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #detects contours
        if len(contours) != 0:
            mouse = cv2.moments(thresh) #centroid of the largest contour
            cX = (int(mouse["m10"] / mouse["m00"])
            cY = (int(mouse["m01"] / mouse["m00"]))
            
            x = -(center - cX) if cX < center else cX - center
            y = -(center - cY) if cY < center else cY - center
            
            x2 = x * speed
            y2 = y * speed
                
            mousemove(x2,y2)