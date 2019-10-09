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

min_max_scaler = MinMaxScaler()
#from RealSenseCamera import RealSenseCamera
lower=np.array([76,0,16])
upper=np.array([163, 79, 100])

l2=np.array([76,0,16])
u2=np.array([163, 79, 100])

pl=np.array([0,0,0])
pu=np.array([87,94,255])
file = open('real_record.pkl', 'rb')
frames = pickle.load(file)
file.close()
pic=0
k = 60
# for frame in frames:
for i in range(0, len(frames), k):
    frame = frames[i]
    pic=pic+1
    color_image = frame['color_image']
    depth_image = frame['depth_image']
    hsv=cv2.cvtColor(color_image,cv2.COLOR_BGR2HSV)
    hsl=cv2.cvtColor(color_image,cv2.COLOR_BGR2HLS)
    mask=cv2.inRange(hsv,lower,upper)
    plantMask=cv2.inRange(hsl,pl,pu)
    finalmask=mask



    mask=cv2.Canny(finalmask,100,150)
    lines = cv2.HoughLinesP(mask, 1, np.pi/180, 100, minLineLength=10, maxLineGap=250)
    l1x1,l1x2,l1y1,l1y2=0,0,0,0
    l2x1,l2x2,l2y1,l2y2=0,0,0,0
    l1=0
    l2=0
    dd=0
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
    if(l1 + l2 == 0):
        continue
    dd /= (l1 + l2);

    cv2.imshow('plant',plantMask)
    x,y,w,h=0,0,0,0
    font = cv2.FONT_HERSHEY_SIMPLEX
    contours,heirarchy=cv2.findContours(plantMask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if(contours is not None):
        areas=[cv2.contourArea(cnt) for cnt in contours]
        index=np.argmax(areas)
        x,y,w,h=cv2.boundingRect(contours[index])
        depth=depth_image[y:y+h,x:x+w]

        for i in list1:
            if(i[0] >= x and i[0] <= x + w and i[1] >= y and i[1] <= y + h):
                text=str(depth.max())
                ht = int(float(text));
                if( ht >= dd + 100):
                    cv2.putText(color_image,text,(x,y), font, 2,(255,255,255),2,cv2.LINE_AA)
                    cv2.rectangle(color_image,(x,y),(x+w,y+h),(0,0,255),4)
                    print(x, y, x+w, y+h, text)
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
