from xml.dom.minidom import Document
import xml.etree.cElementTree as ET


def save_to_xml(save_path, folder_name, im_width, im_height, im_depth, objects_axis, label_name):
    object_num = len(objects_axis)
    doc = Document()
    file_name = save_path.split('/')[-1]

    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)

    folder = doc.createElement('folder')
    folder.appendChild(doc.createTextNode(folder_name))
    annotation.appendChild(folder)

    path = doc.createElement('path')
    path.appendChild(doc.createTextNode(save_path))
    annotation.appendChild(path)

    filename = doc.createElement('filename')
    filename.appendChild(doc.createTextNode(file_name))
    annotation.appendChild(filename)

    source = doc.createElement('source')
    annotation.appendChild(source)

    database = doc.createElement('database')
    database.appendChild(doc.createTextNode('Unknown'))
    source.appendChild(database)

    size = doc.createElement('size')
    annotation.appendChild(size)

    # 需要修改的就是这部分，宽高
    width = doc.createElement('width')
    width.appendChild(doc.createTextNode(str(im_width)))
    height = doc.createElement('height')
    height.appendChild(doc.createTextNode(str(im_height)))
    depth = doc.createElement('depth')
    depth.appendChild(doc.createTextNode(str(im_depth)))
    size.appendChild(width)
    size.appendChild(height)
    size.appendChild(depth)

    segmented = doc.createElement('segmented')
    segmented.appendChild(doc.createTextNode('0'))
    annotation.appendChild(segmented)

    # 需要添加目标
    for i in range(object_num):
        objects = doc.createElement('object')
        annotation.appendChild(objects)
        object_name = doc.createElement('name')
        object_name.appendChild(doc.createTextNode(label_name[int(objects_axis[i][4])]))
        objects.appendChild(object_name)
        pose = doc.createElement('pose')
        pose.appendChild(doc.createTextNode('Unspecified'))
        objects.appendChild(pose)
        truncated = doc.createElement('truncated')
        truncated.appendChild(doc.createTextNode('0'))
        objects.appendChild(truncated)
        difficult = doc.createElement('difficult')
        difficult.appendChild(doc.createTextNode('0'))
        objects.appendChild(difficult)
        bndbox = doc.createElement('bndbox')
        objects.appendChild(bndbox)
        xmin = doc.createElement('xmin')
        xmin.appendChild(doc.createTextNode(str(objects_axis[i][0])))
        bndbox.appendChild(xmin)
        ymin = doc.createElement('ymin')
        ymin.appendChild(doc.createTextNode(str(objects_axis[i][1])))
        bndbox.appendChild(ymin)
        xmax = doc.createElement('xmax')
        xmax.appendChild(doc.createTextNode(str(objects_axis[i][2])))
        bndbox.appendChild(xmax)
        ymax = doc.createElement('ymax')
        ymax.appendChild(doc.createTextNode(str(objects_axis[i][3])))
        bndbox.appendChild(ymax)

    return doc
    # f = open(save_path, 'w')
    # f.write(doc.toprettyxml())
    # f.close()


def load_from_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    box = []
    label = []
    id = {}
    label_num = 0
    label_set = set()

    for obj in root.findall('object'):
        name = obj.find('name').text
        if not (name in label_set):
            id[name] = label_num
            label.append(name)
            label_set.add(name)
            label_num += 1

        boxid = id[name]

        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        box.append([xmin, ymin, xmax, ymax, boxid])

    return box, label
