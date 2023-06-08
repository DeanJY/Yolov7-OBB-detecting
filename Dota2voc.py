import os
import cv2
from xml.dom.minidom import Document 
 
#windows下无需
# import sys  
# stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
# sys.setdefaultencoding('utf-8')
# sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde
 
 
category_set = ['bus', 'Pkw', 'Truck', 'truck_trail', 'van_trail', 'cam', 'pkw_trail']  
 
def custombasename(fullname):  
    return os.path.basename(os.path.splitext(fullname)[0])
 
 
def limit_value(a,b):
    if a<1:
        a = 1
    if a>=b:
        a = b-1
    return a
 
    
def readlabeltxt(txtpath, height, width, hbb = True):
    print(txtpath)
    with open(txtpath, 'r') as f_in:   #打开txt文件          
        lines = f_in.readlines()
        splitlines = [x.strip().split(' ') for x in lines]  #根据空格分割
        boxes = []
        for i, splitline  in enumerate(splitlines):
            # if i in [0,1]:  #DOTA数据集前两行对于我们来说是无用的
            #     continue
            label = splitline[8]
            angel = splitline[10]
            if label not in category_set:#只书写制定的类别      
                continue            
            x1 = int(float(splitline[0]))
            y1 = int(float(splitline[1]))
            x2 = int(float(splitline[2]))
            y2 = int(float(splitline[3]))
            x3 = int(float(splitline[4]))
            y3 = int(float(splitline[5]))  
            x4 = int(float(splitline[6]))
            y4 = int(float(splitline[7]))
            #如果是hbb
            if hbb:
                xx1 = min(x1,x2,x3,x4)
                xx2 = max(x1,x2,x3,x4)
                yy1 = min(y1,y2,y3,y4)
                yy2 = max(y1,y2,y3,y4)
                
                xx1 = limit_value(xx1, width)
                xx2 = limit_value(xx2, width)
                yy1 = limit_value(yy1, height)
                yy2 = limit_value(yy2, height)
                
                box = [xx1,yy1,xx2,yy2,label,angel]
                boxes.append(box)            
            else:  #否则是obb                        
                x1 = limit_value(x1, width)
                y1 = limit_value(y1, height)
                x2 = limit_value(x2, width)
                y2 = limit_value(y2, height)
                x3 = limit_value(x3, width)
                y3 = limit_value(y3, height)   
                x4 = limit_value(x4, width)
                y4 = limit_value(y4, height)
                               
                box = [x1,y1,x2,y2,x3,y3,x4,y4,label]
                boxes.append(box)
    return boxes

#旋转框格式 
def writeXml(tmp, imgname, w, h, d, bboxes, hbb = True):  
    doc = Document()  
    #owner  
    annotation = doc.createElement('annotation')  
    doc.appendChild(annotation)  
    #owner  
    folder = doc.createElement('folder')  
    annotation.appendChild(folder)  
    folder_txt = doc.createTextNode("JPEGImages")  
    folder.appendChild(folder_txt)  
  
    filename = doc.createElement('filename')  
    annotation.appendChild(filename)  
    filename_txt = doc.createTextNode(imgname)  
    filename.appendChild(filename_txt) 

    path =  doc.createElement('path')
    annotation.appendChild(path)
    path_txt = doc.createTextNode("JPEGImages")
    path.appendChild(path_txt)
    #ones#  
    source = doc.createElement('source')  
    annotation.appendChild(source)  
  
    database = doc.createElement('database')  
    source.appendChild(database)  
    database_txt = doc.createTextNode("DLR 3K")  
    database.appendChild(database_txt)  
  
    annotation_new = doc.createElement('annotation')  
    source.appendChild(annotation_new)  
    annotation_new_txt = doc.createTextNode("VOC2007")  
    annotation_new.appendChild(annotation_new_txt)  
  
    image = doc.createElement('image')  
    source.appendChild(image)  
    image_txt = doc.createTextNode("flickr")  
    image.appendChild(image_txt) 
    # #owner
    # owner = doc.createElement('owner')  
    # annotation.appendChild(owner)  
  
    # flickrid = doc.createElement('flickrid')  
    # owner.appendChild(flickrid)  
    # flickrid_txt = doc.createTextNode("NULL")  
    # flickrid.appendChild(flickrid_txt) 
    
    # ow_name = doc.createElement('name')  
    # owner.appendChild(ow_name)  
    # ow_name_txt = doc.createTextNode("idannel")  
    # ow_name.appendChild(ow_name_txt)
    #onee#  
    #twos#  
    size = doc.createElement('size')  
    annotation.appendChild(size)  
  
    width = doc.createElement('width')  
    size.appendChild(width)  
    width_txt = doc.createTextNode(str(w))  
    width.appendChild(width_txt)  
  
    height = doc.createElement('height')  
    size.appendChild(height)  
    height_txt = doc.createTextNode(str(h))  
    height.appendChild(height_txt)  
  
    depth = doc.createElement('depth') 
    size.appendChild(depth)  
    depth_txt = doc.createTextNode(str(d))  
    depth.appendChild(depth_txt)  
    #twoe#  
    segmented = doc.createElement('segmented')  
    annotation.appendChild(segmented)  
    segmented_txt = doc.createTextNode("0")  
    segmented.appendChild(segmented_txt)  
    
    for bbox in bboxes:
        #threes#  
        object_new = doc.createElement("object")  
        annotation.appendChild(object_new)  
        
        name = doc.createElement('name')  
        object_new.appendChild(name)  
        name_txt = doc.createTextNode(str(bbox[8]))  
        name.appendChild(name_txt)  
  
        pose = doc.createElement('pose')  
        object_new.appendChild(pose)  
        pose_txt = doc.createTextNode("Unspecified")  
        pose.appendChild(pose_txt)  
  
        truncated = doc.createElement('truncated')  
        object_new.appendChild(truncated)  
        truncated_txt = doc.createTextNode("0")  
        truncated.appendChild(truncated_txt)  
  
        difficult = doc.createElement('difficult')  
        object_new.appendChild(difficult)  
        difficult_txt = doc.createTextNode("0")  
        difficult.appendChild(difficult_txt) 

        rotated_bndbox = doc.createElement('rotated_bndbox')  
        object_new.appendChild(rotated_bndbox)
        
        rotated_bbox_cx = doc.createElement('rotated_bbox_cx')
        rotated_bndbox.appendChild(rotated_bbox_cx)
        rotated_bbox_cx_txt = doc.createTextNode(str(bbox[9]))
        rotated_bbox_cx.appendChild(rotated_bbox_cx_txt)

        rotated_bbox_cy = doc.createElement('rotated_bbox_cy')
        rotated_bndbox.appendChild(rotated_bbox_cy)
        rotated_bbox_cy_txt = doc.createTextNode(str(bbox[10]))
        rotated_bbox_cy.appendChild(rotated_bbox_cy_txt)

        rotated_bbox_w = doc.createElement('rotated_bbox_w')
        rotated_bndbox.appendChild(rotated_bbox_w)
        rotated_bbox_w_txt = doc.createTextNode(str(bbox[11]))
        rotated_bbox_w.appendChild(rotated_bbox_w_txt)

        rotated_bbox_h = doc.createElement('rotated_bbox_h')
        rotated_bndbox.appendChild(rotated_bbox_h)
        rotated_bbox_h_txt = doc.createTextNode(str(bbox[12]))
        rotated_bbox_h.appendChild(rotated_bbox_h_txt)

        rotated_bbox_theta = doc.createElement('rotated_bbox_theta')
        rotated_bndbox.appendChild(rotated_bbox_theta)
        rotated_bbox_theta_txt = doc.createTextNode(str(bbox[13]))
        rotated_bbox_theta.appendChild(rotated_bbox_theta_txt)    
    
        x1 = doc.createElement('x1')  
        rotated_bndbox.appendChild(x1)  
        x1_txt = doc.createTextNode(str(bbox[0]))
        x1.appendChild(x1_txt)  
    
        y1 = doc.createElement('y1')  
        rotated_bndbox.appendChild(y1)  
        y1_txt = doc.createTextNode(str(bbox[1]))
        y1.appendChild(y1_txt) 
        
        x2 = doc.createElement('x2')  
        rotated_bndbox.appendChild(x2)  
        x2_txt = doc.createTextNode(str(bbox[2]))
        x2.appendChild(x2_txt)  
    
        y2 = doc.createElement('y2')  
        rotated_bndbox.appendChild(y2)  
        y2_txt = doc.createTextNode(str(bbox[3]))
        y2.appendChild(y2_txt)
    
        x3 = doc.createElement('x3')  
        rotated_bndbox.appendChild(x3)  
        x3_txt = doc.createTextNode(str(bbox[4]))
        x3.appendChild(x3_txt)  
    
        y3 = doc.createElement('y3')  
        rotated_bndbox.appendChild(y3)  
        y3_txt = doc.createTextNode(str(bbox[5]))
        y3.appendChild(y3_txt)

        x4 = doc.createElement('x4')  
        rotated_bndbox.appendChild(x4)  
        x4_txt = doc.createTextNode(str(bbox[6]))
        x4.appendChild(x4_txt)  
    
        y4 = doc.createElement('y4')  
        rotated_bndbox.appendChild(y4)  
        y4_txt = doc.createTextNode(str(bbox[7]))
        y4.appendChild(y4_txt)
    
    xmlname = os.path.splitext(imgname)[0]  
    tempfile = os.path.join(tmp ,xmlname+'.xml')
    with open(tempfile, 'wb') as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
    return  

#正常框格式
def writeXmlf(tmp, imgname, w, h, d, bboxes, hbb = True):  
    
    doc = Document()  
    #owner  
    annotation = doc.createElement('annotation')  
    doc.appendChild(annotation)  
    #owner  
    folder = doc.createElement('folder')  
    annotation.appendChild(folder)  
    folder_txt = doc.createTextNode("JPEGImages")  
    folder.appendChild(folder_txt)  
  
    filename = doc.createElement('filename')  
    annotation.appendChild(filename)  
    filename_txt = doc.createTextNode(imgname)  
    filename.appendChild(filename_txt) 

    path =  doc.createElement('path')
    annotation.appendChild(path)
    path_txt = doc.createTextNode("JPEGImages")
    path.appendChild(path_txt)
    #ones#  
    source = doc.createElement('source')  
    annotation.appendChild(source)  
  
    database = doc.createElement('database')  
    source.appendChild(database)  
    database_txt = doc.createTextNode("DLR 3K")  
    database.appendChild(database_txt)  
  
    annotation_new = doc.createElement('annotation')  
    source.appendChild(annotation_new)  
    annotation_new_txt = doc.createTextNode("VOC2007")  
    annotation_new.appendChild(annotation_new_txt)  
  
    image = doc.createElement('image')  
    source.appendChild(image)  
    image_txt = doc.createTextNode("flickr")  
    image.appendChild(image_txt) 
    # #owner
    # owner = doc.createElement('owner')  
    # annotation.appendChild(owner)  
  
    # flickrid = doc.createElement('flickrid')  
    # owner.appendChild(flickrid)  
    # flickrid_txt = doc.createTextNode("NULL")  
    # flickrid.appendChild(flickrid_txt) 
    
    # ow_name = doc.createElement('name')  
    # owner.appendChild(ow_name)  
    # ow_name_txt = doc.createTextNode("idannel")  
    # ow_name.appendChild(ow_name_txt)
    #onee#  
    #twos#  
    size = doc.createElement('size')  
    annotation.appendChild(size)  
  
    width = doc.createElement('width')  
    size.appendChild(width)  
    width_txt = doc.createTextNode(str(w))  
    width.appendChild(width_txt)  
  
    height = doc.createElement('height')  
    size.appendChild(height)  
    height_txt = doc.createTextNode(str(h))  
    height.appendChild(height_txt)  
  
    depth = doc.createElement('depth') 
    size.appendChild(depth)  
    depth_txt = doc.createTextNode(str(d))  
    depth.appendChild(depth_txt)  
    #twoe#  
    segmented = doc.createElement('segmented')  
    annotation.appendChild(segmented)  
    segmented_txt = doc.createTextNode("0")  
    segmented.appendChild(segmented_txt)  
    
    for bbox in bboxes:
        #计算框框值
        xmin_f = bbox[9]-bbox[11]
        ymin_f = bbox[10]-bbox[12]
        xmax_f = bbox[9]+bbox[11]
        ymax_f = bbox[10]+bbox[12]
        #threes#  
        object_new = doc.createElement("object")  
        annotation.appendChild(object_new)  
        
        name = doc.createElement('name')  
        object_new.appendChild(name)  
        name_txt = doc.createTextNode(str(bbox[8]))  
        name.appendChild(name_txt)  
  
        pose = doc.createElement('pose')  
        object_new.appendChild(pose)  
        pose_txt = doc.createTextNode("Unspecified")  
        pose.appendChild(pose_txt)  
  
        truncated = doc.createElement('truncated')  
        object_new.appendChild(truncated)  
        truncated_txt = doc.createTextNode("0")  
        truncated.appendChild(truncated_txt)  
  
        difficult = doc.createElement('difficult')  
        object_new.appendChild(difficult)  
        difficult_txt = doc.createTextNode("0")  
        difficult.appendChild(difficult_txt) 
  
        bndbox = doc.createElement('bndbox')  
        object_new.appendChild(bndbox)  
  
    
        xmin = doc.createElement('xmin')  
        bndbox.appendChild(xmin)  
        xmin_txt = doc.createTextNode(str(xmin_f))
        xmin.appendChild(xmin_txt)  

        ymin = doc.createElement('ymin')  
        bndbox.appendChild(ymin)  
        ymin_txt = doc.createTextNode(str(ymin_f))
        ymin.appendChild(ymin_txt)    

        xmax = doc.createElement('xmax')  
        bndbox.appendChild(xmax)  
        xmax_txt = doc.createTextNode(str(xmax_f))
        xmax.appendChild(xmax_txt)  
    
        ymax = doc.createElement('ymax')  
        bndbox.appendChild(ymax)  
        ymax_txt = doc.createTextNode(str(ymax_f))
        ymax.appendChild(ymax_txt) 
        
    
    xmlname = os.path.splitext(imgname)[0]  
    tempfile = os.path.join(tmp ,xmlname+'.xml')
    with open(tempfile, 'wb') as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
    return    
 
 
if __name__ == '__main__':
    data_path = 'MunichDatasetVehicleDetection-2015-old/Annotations'
    # images_path = os.path.join(data_path, 'images') #样本图片路径
    # labeltxt_path = os.path.join(data_path, 'labelTxt') #DOTA标签的所在路径
    images_path = 'MunichDatasetVehicleDetection-2015-old/img'
    labeltxt_path = 'MunichDatasetVehicleDetection-2015-old/label' 
    anno_new_path = os.path.join(data_path, 'obbxml')  #新的voc格式存储位置（hbb形式）
    ext = '.JPG'  #样本图片的后缀
    filenames=os.listdir(labeltxt_path)    #获取每一个txt的名称   
    for filename in filenames:    
        filepath=labeltxt_path + '/'+filename    #每一个DOTA标签的具体路径
        picname = os.path.splitext(filename)[0] + ext  
        pic_path = os.path.join(images_path, picname) 
        im= cv2.imread(pic_path)            #读取相应的图片               
        (H,W,D) = im.shape                  #返回样本的大小
        boxes = readlabeltxt(filepath, H, W, hbb = True)           #默认是矩形（hbb）得到gt
        print(len(boxes))
        if len(boxes)==0:
            print('文件为空',filepath)
        #读取对应的样本图片，得到H,W,D用于书写xml
 
        #书写xml
        writeXml(anno_new_path, picname, W, H, D, boxes, hbb = True)
        print('正在处理%s'%filename)