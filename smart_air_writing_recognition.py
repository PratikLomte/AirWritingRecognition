##Updated

##Smart Air Writing Recognition System


import numpy as np
import cv2
from collections import deque
#from threading import Event
import time
from threading import Timer

def setValues(x):
   print("")


# Trackbar Creation
cv2.namedWindow("HSV Trackbars")
cv2.createTrackbar("Max Hue", "HSV Trackbars", 153, 180,setValues)
cv2.createTrackbar("Max Saturation", "HSV Trackbars", 255, 255,setValues)
cv2.createTrackbar("Max Value", "HSV Trackbars", 255, 255,setValues)
cv2.createTrackbar("Min Hue", "HSV Trackbars", 64, 180,setValues)
cv2.createTrackbar("Min Saturation", "HSV Trackbars", 72, 255,setValues)
cv2.createTrackbar("Min Value", "HSV Trackbars", 49, 255,setValues)


#Creation of Deques for the different colors
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]


#Index Values for the different colours
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

kernel = np.ones((5,5),np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0


#Canvas Window Setup
paintWindow = np.zeros((471,636,3)) + 255
paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), colors[3], -1)

cv2.putText(paintWindow, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_ITALIC, 0.5, (150,150,150), 2, cv2.LINE_AA)
cv2.namedWindow('Canvas', cv2.WINDOW_AUTOSIZE)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    #Flipping the frame 
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    u_hue = cv2.getTrackbarPos("Max Hue", "HSV Trackbars")
    u_saturation = cv2.getTrackbarPos("Max Saturation", "HSV Trackbars")
    u_value = cv2.getTrackbarPos("Max Value", "HSV Trackbars")
    l_hue = cv2.getTrackbarPos("Min Hue", "HSV Trackbars")
    l_saturation = cv2.getTrackbarPos("Min Saturation", "HSV Trackbars")
    l_value = cv2.getTrackbarPos("Min Value", "HSV Trackbars")
    Upper_hsv = np.array([u_hue,u_saturation,u_value])
    Lower_hsv = np.array([l_hue,l_saturation,l_value])

    frame = cv2.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
    frame = cv2.rectangle(frame, (160,1), (255,65), colors[0], -1)
    frame = cv2.rectangle(frame, (275,1), (370,65), colors[1], -1)
    frame = cv2.rectangle(frame, (390,1), (485,65), colors[2], -1)
    frame = cv2.rectangle(frame, (505,1), (600,65), colors[3], -1)
    cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

    Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)

    cnts,_ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    center = None

    stp = 0
    
    # Contour Detection
    if len(cnts) > 0:
        
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)

        # For Centroid Calculation
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        
        if center[1] <= 65:
            if 40 <= center[0] <= 140: # For Clear Button
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]

                blue_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0

                paintWindow[67:,:,:] = 255
            elif 160 <= center[0] <= 255:
                    colorIndex = 0 # For Blue Color
            elif 275 <= center[0] <= 370:
                    colorIndex = 1 # For Green Color
            elif 390 <= center[0] <= 485:
                    colorIndex = 2 # For Red Color
            elif 505 <= center[0] <= 600:
                    colorIndex = 3 # For Yellow Color
        else :
            if colorIndex == 0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex == 1:
                gpoints[green_index].appendleft(center)
            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)
            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)
    else:
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1

    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue


                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

                if True:

                   def delay():
                      print('')

                   clk = Timer(0.0005,delay)  
                   clk.start()

                   
                   #Event().wait(.05)
                   #event = Event()
                   #event.wait(0.5)
                   #time.sleep(0.5)
                   #for i in range(60):
                      #sleep(1)

                   
                   def pause_key(keypress, seconds):
                      key = 0
                      print('Space')

                      
                      for second in range(seconds):
                         input_kb = cv2.waitKey(2) & 0xFF
                         if input_kb == ord(' '):
                            print('paused')
                            cv2.waitKey(0)
                            print('continued')
                         time.sleep(1)
                         print(second)
                         second += 1
                         break
                           

                     


                 
                #cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                #cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

                #if __name__ == '__main__':
                 #  pause_key(keypress=' ', seconds=10)
                




                ###Tried the same with waitkey, with "s" As keyboard interrupt
                 
                #if cv2.waitKey(1) & 0xFF == ord("s"):
                   #break
                   #Event().wait(.025)
                   #cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                   #cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                   #break

                #cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                #cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                

    cv2.imshow("Tracking", frame)
    cv2.imshow("Canvas", paintWindow)
    cv2.imshow("Mask",Mask)


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


#cap.release()
#cv2.destroyAllWindows()
cap.release()
cv2.destroyAllWindows()




