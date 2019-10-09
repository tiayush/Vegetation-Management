from time import sleep
from sklearn.preprocessing import MinMaxScaler
import cv2
import numpy as np
import pickle
import numpy as np
import sys
from db import Trial
orig_stdout = sys.stdout
sys.stdout = open('file.txt', 'w')

#will be used the bring pixel in the range 1 to 255
min_max_scaler = MinMaxScaler()

#from RealSenseCamera import RealSenseCamera

#HSV value to detect black color
lower=np.array([76,0,16])
upper=np.array([163, 79, 100])

l2=np.array([76,0,16])
u2=np.array([163, 79, 100])

#HSV value to detect green color
pl=np.array([0,0,0])
pu=np.array([87,94,255])

#desirilize the file
file = open('real_record.pkl', 'rb')
frames = pickle.load(file)
file.close()


#Configurable frame jump key
k = 70


ct = 0
ct1 = 0

#iterating on each frame
for i in range(0, len(frames), k):
    if(ct == 1):
        ct ^= 1
        continue
    ct ^= 1
    frame = frames[i]
    
    #getting the rgb and depth information
    color_image = frame['color_image']
    depth_image = frame['depth_image']

    #converting bgr into hsv image
    hsv=cv2.cvtColor(color_image,cv2.COLOR_BGR2HSV)
    hsl=cv2.cvtColor(color_image,cv2.COLOR_BGR2HLS)
    mask=cv2.inRange(hsv,lower,upper)
    plantMask=cv2.inRange(hsl,pl,pu)
    finalmask=mask



    mask=cv2.Canny(finalmask,100,150)

    #using HoughLines to detect lines in the frame(representing the electrical)
    lines = cv2.HoughLinesP(mask, 1, np.pi/180, 100, minLineLength=10, maxLineGap=250)
    l1x1,l1x2,l1y1,l1y2=0,0,0,0
    l2x1,l2x2,l2y1,l2y2=0,0,0,0
    l1=0
    l2=0
    dd=0
    
    #iteration on each line and storing the coordinates
    list1 = []
    if(lines is not None):
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope=(y2-y1)/(x2-x1+1)
            if(abs(slope)<0.2):
                if(y1<200):
                    l1x1+=x1
                    l1x2+=x2
                    l1y1+=y1
                    l1y2+=y2
                    l1=l1+1
                else:
                    l2x1+=x1
                    l2x2+=x2
                    l2y1+=y1
                    l2y2+=y2
                    l2=l2+1
        if(l1!=0 and l2!=0):
            l1x1=l1x1/l1
            l1x2=l1x2/l1
            l1y1=l1y1/l1
            l1y2=l1y2/l1

            l2x1=l2x1/l2
            l2x2=l2x2/l2
            l2y1=l2y1/l2
            l2y2=l2y2/l2
            cv2.line(color_image, (int(l1x1), int(l1y1)), (int(l1x2), int(l1y2)), (0, 255, 0), 3)
            cv2.line(color_image, (int(l2x1), int(l2y1)), (int(l2x2), int(l2y2)), (0, 255, 0), 3)
            list1.append([l1x1, l1y1])
            list1.append([l1x2, l1y2])
            list1.append([l2x1, l2y1])
            list1.append([l2x2, l2y2])
            
            dd += depth_image[min(479, int(l1x1))][min(640-1,int(l1y1))]
            dd += depth_image[min(479, int(l1x2))][min(640-1, int(l1y2))]
            dd += depth_image[min(479, int(l2x1))][min(640-1, int(l2y1))]
            dd += depth_image[min(480-1, int(l2x2))][min(640-1, int(l2y2))]
    # if(ct == 0):
    #     continue
    dd /= 1.75

   # print(dd)

    #converting the plants into black & white hsv Mask
    cv2.imshow('plant',plantMask)
    x,y,w,h=0,0,0,0

    #Font used to display ALERT
    font = cv2.FONT_HERSHEY_SIMPLEX

    #finding contours using height of the tree as a pramater
    contours,heirarchy=cv2.findContours(plantMask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if(contours is not None):
        areas=[cv2.contourArea(cnt) for cnt in contours]
        index=np.argmax(areas)
        x,y,w,h=cv2.boundingRect(contours[index])
        depth=depth_image[y:y+h,x:x+w]
        for i in list1:
            if(i[0] >= x and i[0] <= x + w and i[1] >= y and i[1] <= y + h):
                text=str(depth.max())
                text1 = "ALERT"
                ht = int(float(text))
                if(ht > 5000):
                    cv2.putText(color_image,text1,(x,y), font, 2,(255,255,255),2,cv2.LINE_AA)
                
                #drawing red color bounding box around the trees below the wire
                cv2.rectangle(color_image,(x,y),(x+w,y+h),(0,0,255),4)
                print(x, y, x+w, y+h, text)
                ct1 += 1
                # print(text)
                break
        
            

    cv2.imshow('s',color_image)
    cv2.waitKey(1)
    sleep(2)
sys.stdout.close()
sys.stdout=orig_stdout 


#code for database started here.
sqlA = Trial()
f = open('file.txt', "r")
lines = list(f)
f.close()

command = sqlA.maketable()
for i in lines:
    i = i.replace("\n", "")
    l = i.split(' ')
    l = list(map(int, l))
    command = sqlA.makeinsert("TREES",l[0],l[1],l[2],l[3],l[4])
    sqlA.put_record(command)
    # command = sqlA.makeinsert("TREES",5,2)
    # sqlA.put_record(command)
    # query=sqlA.make_query("TREES","2")
    # sqlA.read_record(query)]

command = sqlA.make_query("TREES", "1400")
sqlA.read_record(command)
