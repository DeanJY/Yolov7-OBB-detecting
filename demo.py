import glob
import os
from PIL import Image
import numpy as np
# nfiles = glob.glob("data"+"/*.JPG")
# nfiles.sort()
# for file in nfiles:
#     img = Image.open(file)
#     file_name = file.split(".JPG")[0]
#     # img.show()
#     # print(file_name)
#     # print(file_name.split("data/")[1])
#     # x =1
#     # a = file_name.split("data/")[1] +"_{}_{}".format(x,x)
#     # print(a)
#     x = 1
#     y =1
#     output_txt_folder = 'MunichDatasetVehicleDetection-2015-old/Annotations'
#     output_name = file_name.split("data/")[1] + "_{}_{}".format(x,y)
#     output_img = output_name + ".jpg"
#     output_txt = output_name + ".txt"
#     path_txt = output_txt_folder +"/"+ output_txt
#     print(path_txt)
#     tempfile = os.path.join(output_txt_folder ,output_name+'.xml')
#     print(tempfile)
a = [2,4,6,1,3,9,5,2]
a.sort(reverse=True)
print(a)
# top_10_max_elements = sorted(enumerate(a), key=lambda x: x[1], reverse=True)[:3]

# # 输出前十个最大元素及其索引
# for idx, value in top_10_max_elements:
#     print("元素：", value, "索引：", idx)

