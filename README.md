# python - VOC 文件的接口
#### save_to_xml(save_path, folder_name, im_width, im_height, im_depth, objects_axis, label_name)
objects_axis: 一个n个5-D向量，[x0, y0 , x1, y1, label_id]  
label_name: 一个dictionary，label_id -> label_name

#### load_from_xml()
返回: object_axis, label_name
