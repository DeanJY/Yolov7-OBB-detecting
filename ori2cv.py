from fileinput import filename
from importlib.metadata import files
import os
import glob
from sys import flags
import numpy as np
import math
import cv2
def rotate_rect(center_x, center_y, width, height, angle):
    # 将角度转换为弧度
    theta = math.radians(angle)
    # 计算旋转后的左上角顶点坐标
    a =  -width
    b =  -height
    c =  width
    d =  height
    (x1,y1) = (a*math.cos(theta)+b*math.sin(theta)+center_x,-a*math.sin(theta)+b*math.cos(theta)+center_y)
    (x2,y2) = (a*math.cos(theta)+d*math.sin(theta)+center_x,-a*math.sin(theta)+d*math.cos(theta)+center_y)
    (x3,y3) = (c*math.cos(theta)+b*math.sin(theta)+center_x,-c*math.sin(theta)+b*math.cos(theta)+center_y)
    (x4,y4) = (c*math.cos(theta)+d*math.sin(theta)+center_x,-c*math.sin(theta)+d*math.cos(theta)+center_y) 

    # 返回旋转后的四个顶点坐标
    return (x1,y1),(x2,y2),(x3,y3),(x4,y4)

class_dict = {"10":"Pkw","11":"pkw_trail","22":"Truck", "23":"truck_trail","17":"van_trail","20":"cam","30":"bus"}
classes = ['bus', 'pkw', 'truck', 'truck_trail', 'van_trail', 'cam', 'pkw_trail']
nfiles = glob.glob("data"+"/*.JPG")
nfiles.sort()
for file in nfiles:
    file_name = file.split(".JPG")[0]
    #data/2012-04-26-Muenchen-Tunnel_4K0G0010
    for class_name in classes:
        if class_name != 'pkw':
            continue
        file_path = file_name +"_" + class_name + ".samp"
        if os.path.exists(file_path):
            print(file_path)
            txt = open(file_path,'r')
            image = cv2.imread(file)
            txt_data = txt.readlines()
            flag = False
            count_10 = 0
            count_16 = 0
            for row in txt_data:
                if row.split(":")[0] == "# format":
                    flag = True
                   
                elif flag:
                    id,id_class,center_x,center_y,w,h,angle = map(float,row.split(" "))
                    if w == 0:
                        continue
                    
                    (x1,y1),(x2,y2),(x3,y3),(x4,y4) = rotate_rect(center_x,center_y, w,h,angle) 
                    pts = np.array([(x1,y1),(x2,y2),(x4,y4),(x3,y3)], np.int32)
                    pts = pts.reshape((-1,1,2))
                    
                    if id_class ==16:
                        color = (0,255,0)  
                        count_16 +=1
                    else:
                        color = (255,0,0)
                        count_10  +=1
                    thickness = 2     # 线条宽度
                    isClosed = True   # 是否闭合
                    cv2.polylines(image, [pts], isClosed, color, thickness)
            img_path =  './{}.jpg'.format("123") 
            print(img_path)
            cv2.imwrite(img_path, image)
            print(count_10,count_16)
    break