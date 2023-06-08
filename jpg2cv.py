import imghdr
from itertools import cycle
from multiprocessing.spawn import import_main_path
from re import A
import xml.etree.ElementTree as ET
import os, cv2
import xml
# ------------------------------------------------------
#           可视化一张图片
# ------------------------------------------------------
def read_xml_one(xml_file, img_file):
    
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # imgfile='C:/Users/nansbas/Desktop/01_000002_01244-01086_0939-0989.jpg'
    im = cv2.imread(img_file)
    print(im)
    for object in root.findall('object'):
        object_name = object.find('name').text
        print(object_name)
        Xmin = int(object.find('bndbox').find('xmin').text)
        Ymin = int(object.find('bndbox').find('ymin').text)
        Xmax = int(object.find('bndbox').find('xmax').text)
        Ymax = int(object.find('bndbox').find('ymax').text)
        color = (4, 250, 7)
        cv2.rectangle(im, (Xmin, Ymin), (Xmax, Ymax), color, 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(im, object_name, (Xmin, Ymin - 7), font, 0.5, (6, 230, 230), 2)
        # cv2.imshow('01',im)
        print(im)
        cv2.imwrite('./2.jpg', im)


# ---------------------------------------------------
# 可视化文件夹中所有xml文件 #
# ---------------------------------------------------
type45="i2,i4,i5,il100,il60,il80,io,ip,p10,p11,p12,p19,p23,p26,p27,p3,p5,p6,pg,ph4,ph4.5,ph5,pl100,pl120,pl20,pl30,pl40,pl5,pl50,pl60,pl70,pl80,pm20,pm30,pm55,pn,pne,po,pr40,w13,w32,w55,w57,w59,wo"
type45 = type45.split(',')
type45_dic = {}
for item in type45:
    type45_dic[item] = 0
# print(type45_dic)
print(len(type45_dic))
# classes = {'1_23': 0, '3_24_n40': 0, '5_20': 0, '5_16': 0, '5_19_1': 0, '2_1': 0, '2_4': 0, '4_1_1': 0, '3_27': 0, '5_15_2': 0}
def read_xml(ImgPath, AnnoPath, Savepath):
    i = 0
    count = 0
    imagelist = os.listdir(AnnoPath)
    # print(imagelist)
    for image in imagelist:
        image_pre, ext = os.path.splitext(image)
        imgfile = ImgPath + '\\' + image_pre + '.jpg'
        xmlfile = AnnoPath + '\\' + image_pre + '.xml'
        im = cv2.imread(imgfile)
        DomTree = xml.dom.minidom.parse(xmlfile)
        annotation = DomTree.documentElement
        filenamelist = annotation.getElementsByTagName('filename')
        filename = filenamelist[0].childNodes[0].data
        objectlist = annotation.getElementsByTagName('object')

        for objects in objectlist:
            count += 1

            namelist = objects.getElementsByTagName('name')
            objectname = namelist[0].childNodes[0].data
            # if objectname not in classes:
            #     classes[objectname] = 0
            if objectname not in type45:
                # type45[objectname] = 0
                continue
            type45_dic[objectname] += 1

            bndbox = objects.getElementsByTagName('bndbox')

            for box in bndbox:
                i += 1
                try:
                    x1_list = box.getElementsByTagName('xmin')
                    x1 = round(float(x1_list[0].childNodes[0].data))
                    y1_list = box.getElementsByTagName('ymin')
                    y1 = round(float(y1_list[0].childNodes[0].data))
                    x2_list = box.getElementsByTagName('xmax')
                    x2 = round(float(x2_list[0].childNodes[0].data))
                    y2_list = box.getElementsByTagName('ymax')
                    y2 = round(float(y2_list[0].childNodes[0].data))
                    #
                    minX = x1
                    minY = y1
                    maxX = x2
                    maxY = y2

                    if (i % 9 == 0):
                        color = (128, 0, 0)
                    elif (i % 9 == 1):
                        color = (153, 51, 0)
                    elif (i % 9 == 2):
                        color = (255, 204, 0)
                    elif (i % 9 == 3):
                        color = (0, 51, 0)
                    elif (i % 9 == 4):
                        color = (51, 204, 204)
                    elif (i % 9 == 5):
                        color = (128, 0, 128)
                    elif (i % 9 == 6):
                        color = (0, 255, 255)
                    elif (i % 9 == 7):
                        color = (60, 179, 113)
                    elif (i % 9 == 8):
                        color = (255, 127, 80)
                    elif (i % 9 == 9):
                        color = (0, 255, 0)
                    cv2.rectangle(im, (x1, y1), (x2, y2), color, 2)
                    # path = Savepath + '/' + image_pre + '.png'
                    # print(path)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(im, objectname, (minX, minY - 7), font, 0.5, color, 2)
                    path_to_save = 'img'
                    cv2.imwrite(path_to_save, im)
                except Exception as e:
                    print(e)
    print(type45_dic)


import math

def rotate_rect(center_x, center_y, width, height, angle):
    # 将角度转换为弧度
    theta = math.radians(angle)
    print(theta)
    # 计算旋转后的左上角顶点坐标
    a =  -width/2
    b =  -height/2
    c =  width/2
    d =  height/2
    print(a,b,c,d)
    (x1,y1) = (a*math.cos(theta)+b*math.sin(theta)+center_x,-a*math.sin(theta)+b*math.cos(theta)+center_y)
    (x2,y2) = (a*math.cos(theta)+d*math.sin(theta)+center_x,-a*math.sin(theta)+d*math.cos(theta)+center_y)
    (x3,y3) = (c*math.cos(theta)+b*math.sin(theta)+center_x,-c*math.sin(theta)+b*math.cos(theta)+center_y)
    (x4,y4) = (c*math.cos(theta)+d*math.sin(theta)+center_x,-c*math.sin(theta)+d*math.cos(theta)+center_y) 

    # 返回旋转后的四个顶点坐标
    return (x1,y1),(x2,y2),(x3,y3),(x4,y4)

if __name__ == '__main__':
    count = 0
    # read_xml_one('VOCdevkit/VOC2007/Annotations/2012-04-26-Muenchen-Tunnel_4K0G0010.xml', 'VOCdevkit/VOC2007/JPEGImages/2012-04-26-Muenchen-Tunnel_4K0G0010.JPG')
    # read_xml('I:\data\VOCdevkit\VOC2007\JPEGImages', 'I:\data\VOCdevkit\VOC2007\Annotations',
    #          'I:\data\\vis_img')
    img = cv2.imread('VOCdevkit/VOC2007/JPEGImages/2012-04-26-Muenchen-Tunnel_4K0G0010.JPG') 
    import numpy as np
    # x1=1877.70
    # y1=1626.43
    # x2=1873.57
    # y2=1663.69
    # x4=1953.99
    # y4=1650.21
    # x3=1949.88
    # y3=1686.33
    c_x =436
    c_y = 1998
    w = 25
    h = 12
    angle = -128.127227
    #436 1998 25 12 -128.157227
    (x1,y1),(x2,y2),(x3,y3),(x4,y4) = rotate_rect(c_x,c_y, w,h,angle) 
    print(x1,y1,x2,y2,x3,y3,x4,y4)
    pts = np.array([(x1,y1),(x2,y2),(x4,y4),(x3,y3)], np.int32)
    pts = pts.reshape((-1,1,2))
    color = (0,255,0)  # 线条颜色
    thickness = 2     # 线条宽度
    isClosed = True   # 是否闭合
    cv2.polylines(img, [pts], isClosed, color, thickness)
    cv2.imwrite('./2.jpg', img)