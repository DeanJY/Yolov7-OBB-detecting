import os
import glob
import numpy as np
import math

class_dict = {"10":"Pkw","11":"pkw_trail","22":"Truck", "23":"truck_trail","17":"van_trail","20":"cam","30":"bus"}
classes = ['bus', 'pkw', 'truck', 'truck_trail', 'van_trail', 'cam', 'pkw_trail']
files = glob.glob("data" + "/*.JPG")
save_path = "data/label/"
files.sort()
for file in files:
    data = ""
    file_name = file.split(".JPG")[0]
    for class_name in classes:
        # if classes.index(class_name) > 1:
        #     class_name = 'bus'
        file_path = file_name + "_" + class_name + ".samp"
        if os.path.exists(file_path):
            file = open(file_path,'r')  #打开文件
            file_data = file.readlines() #读取所有行
            flag = False
            for row in file_data:
                if row.split(":")[0] == "# format":
                    flag = True
                elif flag:
                    # id, id_class, center_x, center_y, width, height, angle = row.split(" ")
                    # angle = float(angle)
                    # diagonal_lenght = math.sqrt(float(width)**2 + float(height)**2)
                    # if float(width) == 0 or id_class == "16":
                    #     continue
                    # diagonal_angle = math.atan(float(height)/float(width)) * 180 / math.pi
                    # new_line = ""
                    # # Beta = diagonal_angle + angle
                    # beta = diagonal_angle + angle
                    # beta_list = [beta, -2 * angle + beta, -180 + beta, -2 * angle - 180 + beta]
                    # for i in range(4):
                    #     point_x = np.round(float(center_x) + diagonal_lenght * math.cos(beta_list[i] * math.pi / 180))
                    #     point_y = np.round(float(center_y) + diagonal_lenght * math.sin(beta_list[i] * math.pi / 180))
                    #     new_line += '{:.1f}'.format(point_x) + " "
                    #     new_line += '{:.1f}'.format(point_y) + " "
                    # print(id_class)
                    # new_line += class_dict[str(id_class)] + " "
                    # new_line += "0" + "\n"
                    # data += new_line
                    id, id_class, center_x, center_y, width, height, angle = map(float, row.split(" "))
                    # diagonal_lenght = math.sqrt(float(width)**2 + float(height)**2)
                    if float(width) == 0 or id_class == 16.0:
                        continue
                    angle = float(angle)
                    # angle = angle / 180 * np.pi
                    # #print(angle)
                    # #print(angle + np.arctan(h / w))
                    # w = width
                    # h = height
                    # cx = center_x
                    # cy = center_y
                    # diagonal = np.sqrt(w ** 2 + h ** 2)
                    # point1_x = np.round(cx + diagonal * np.cos(angle + np.arctan(h / w)))
                    # point1_y = np.round(cy - diagonal * np.sin(angle + np.arctan(h / w)))

                    # point2_x = np.round(cx + diagonal * np.cos(angle - np.arctan(h / w)))
                    # point2_y = np.round(cy - diagonal * np.sin(angle - np.arctan(h / w)))

                    # point3_x = np.round(cx - diagonal * np.cos(angle + np.arctan(h / w)))
                    # point3_y = np.round(cy + diagonal * np.sin(angle + np.arctan(h / w)))

                    # point4_x = np.round(cx - diagonal * np.cos(angle - np.arctan(h / w)))
                    # point4_y = np.round(cy + diagonal * np.sin(angle - np.arctan(h / w)))
                    # new_line = "{} {} {} {} {} {} {} {} ".format(point1_x, point1_y, point2_x, point2_y, point3_x, point3_y, point4_x, point4_y)
                    diagonal_angle = math.atan(float(height)/float(width)) * 180 / math.pi
                    new_line = ""
                    mat_center = [[float(width), float(height)],[-float(width), float(height)],[-float(width), -float(height)],[float(width), -float(height)]]
                    ratate_mat = [[math.cos(angle*math.pi/180), math.sin(angle*math.pi/180)], [-math.sin(angle*math.pi/180), math.cos(angle*math.pi/180)]]
                    mat_center = np.array(mat_center)
                    ratate_mat = np.array(ratate_mat)
                    point_mat =np.dot(ratate_mat, mat_center.T).T + np.array([float(center_x), float(center_y)])   
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
    path_txt = save_path + file_name.split("data/")[-1] + '.txt'
    with open(path_txt, 'w+') as file:
        file.write(data)
    file.close()