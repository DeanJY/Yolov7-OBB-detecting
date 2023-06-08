0、⭐️⭐️⭐️仔细阅读每个py文件中的注释，按照相应注释修改路径和参数

1、使用requirement配置相关环境
2、本程序文档已包含训练完毕模型，可直接进行评测试用，仅保存部分权值文件在log文件夹中，数据集预处理文件位于tool文件夹中
3、图片大小500，700及1000的VOC格式数据集已制作完毕，使用时移到主目录下并改名为VOCdevkit即可.修改yolo.py中的权值文件路径，运行predict.py文件进行预测，运行get_map.py进行测试集评估，结果保存在map_put文件夹中。
4、使用自己的数据集时，请提前制作VOC格式文件夹。
   使用tool/segment.py文件可将DLR数据集分割并制作XML格式标准文件，包括Annatations和JPEGImages文件夹所需文件。
   使用voc_annotation.py文件生成ImageSets文件夹所需文件和2007train.txt，2007val.txt文件，自行配好VOCdevkit文件夹。
   运行train.py文件进行训练，权重模型和训练数据保存在log文件夹中（训练前需提前安装旋转目标检测非极大抑制库，进入到utils\nms_rotated目录之后运行以下命令安装：python setup.py build_ext --inplace）
5、有问题请邮件至Shi_jingao@buaa.edu.cn
