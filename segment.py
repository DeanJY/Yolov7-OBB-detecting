from genericpath import exists
from PIL import Image
import os
import glob
import cv2
import numpy as np
import math
from Dota2voc import writeXml,writeXmlf

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

output_cv_folder = '700*700_f/img'  # 输出文件夹路径
output_txt_folder = '700*700_f/label'
output_xml_folder = '700*700_f/Annotations'
if not os.path.exists(output_cv_folder):
    os.makedirs(output_cv_folder)
if not os.path.exists(output_txt_folder):
    os.makedirs(output_txt_folder)
if not os.path.exists(output_xml_folder):
    os.makedirs(output_xml_folder)
segment_size = (700, 700)  # 分割图像的大小
step_size = (250, 150)  # 步长
class_dict = {"10":"Pkw","11":"pkw_trail","22":"Truck", "23":"truck_trail","17":"van_trail","20":"cam","30":"bus"}
classes = ['bus', 'pkw', 'truck', 'truck_trail', 'van_trail', 'cam', 'pkw_trail']

#数据集路径 改成自己的
files = glob.glob("data"+"/*.JPG")

# 遍历输入文件夹中的所有图像文件
for file in files:
    img = Image.open(file)
    file_name = file.split(".JPG")[0]
    # 计算分割后的图像数量
    segments_x = (img.width - segment_size[0]) // step_size[0] + 2
    segments_y = (img.height - segment_size[1]) // step_size[1] + 2

    # 对图像进行分割并保存
    for y in range(segments_y):
        for x in range(segments_x):
            # 计算当前分割图像的位置和大小
            data = ""
            boxes = []
            left = x * step_size[0]
            top = y * step_size[1]
            right = min(left + segment_size[0], img.width)
            bottom = min(top + segment_size[1], img.height)

            # 如果分割图像宽度不足1000像素，则从右侧开始向左取1000像素进行补全
            if right - left < segment_size[0]:
                left = right - segment_size[0]

            # 如果分割图像高度不足1000像素，则从下侧开始向上取1000像素进行补全
            if bottom - top < segment_size[1]:
                top = bottom - segment_size[1]

            # 裁剪当前分割图像并保存到文件夹中
            segment = img.crop((left, top, right, bottom))

            #遍历当前分割图像中的标签
            for class_name in classes:
                txt_path = file_name + "_" + class_name + ".samp" 
                if os.path.exists(txt_path):
                    txt = open(txt_path,'r')
                    txt_data = txt.readlines()
                    flag = False
                    for row in txt_data:
                        if row.split(":")[0] == "# format":
                            flag = True
                        elif flag:
                            id, id_class, center_x, center_y, width, height, angle = map(float, row.split(" "))
                            if float(width) == 0 or id_class == 16.0:
                                continue 
                            (x1,y1),(x2,y2),(x3,y3),(x4,y4) = rotate_rect(center_x,center_y, width,height,angle) 
                            exist = False
                            if x1>=left and x1<=right and y1>=top and y1<=bottom and \
                                x2>=left and x2<=right and y2>=top and y2<=bottom and \
                                x3>=left and x3<=right and y3>=top and y3<=bottom and \
                                x4>=left and x4<=right and y4>=top and y4<=bottom:
                                exist = True
                            if exist:
                                center_x_seg = center_x - left
                                center_y_seg = center_y - top
                                (x1,y1),(x2,y2),(x3,y3),(x4,y4) = rotate_rect(center_x_seg,center_y_seg, width,height,angle)  
                                label = class_dict[str(int(id_class))]
                                box = [x1,y1,x2,y2,x3,y3,x4,y4,label,center_x_seg,center_y_seg,width,height,angle]
                                boxes.append(box)
                                new_line = ""
                                mat_center = [[float(width), float(height)],[-float(width), float(height)],[-float(width), -float(height)],[float(width), -float(height)]]
                                ratate_mat = [[math.cos(angle*math.pi/180), math.sin(angle*math.pi/180)], [-math.sin(angle*math.pi/180), math.cos(angle*math.pi/180)]]
                                mat_center = np.array(mat_center)
                                ratate_mat = np.array(ratate_mat)
                                point_mat =np.dot(ratate_mat, mat_center.T).T + np.array([float(center_x_seg), float(center_y_seg)])   
                                for i in range(4):
                                    point_x = point_mat[i][0]
                                    point_y = point_mat[i][1]
                                    new_line += '{:.1f}'.format(point_x) + " "
                                    new_line += '{:.1f}'.format(point_y) + " "
                                print(id_class)
                                new_line += class_dict[str(int(id_class))] + " "
                                new_line += "0" + " {}".format(angle) + "\n"
                                # new_line += " {} {}".format((point_mat[0][0]+point_mat[3][0])/2, (point_mat[0][1]+point_mat[3][1])/2) + "\n"
                                data += new_line
                                
            if boxes:
                # 计算输出文件名并保存图像
                output_name = file_name.split("data/")[1] + "_{}_{}".format(x,y)
                output_img = output_name + ".jpg"
                output_txt = output_name + ".txt"
                #(H,W,D) = (1000,1000,3)
                (H,W,D) = (700,700,3)

                
                #obb格式
                writeXml(output_xml_folder,output_img,W,H,D,boxes,hbb=False)
                segment.save(os.path.join(output_cv_folder, output_img))
                # 输出DOTA标签
                path_txt = output_txt_folder + "/"+output_txt
                with open(path_txt, 'w+') as F:
                    F.write(data)
                F.close()

                #非旋转框格式
                # writeXmlf(output_xml_folder,output_img,W,H,D,boxes,hbb=False)
                # segment.save(os.path.join(output_cv_folder, output_img))
