import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
sets = ['train', 'test', 'val']
classes = [
    "i1",
    "i10",
    "i11",
    "i12",
    "i13",
    "i14",
    "i15",
    "i2",
    "i3",
    "i4",
    "i5",
    "i6",
    "i7",
    "i8",
    "i9",
    "il50",
    "ip",
    "p1",
    "p10",
    "p11",
    "p12",
    "p13",
    "p14",
    "p15",
    "p16",
    "p17",
    "p18",
    "p19",
    "p2",
    "p20",
    "p21",
    "p22",
    "p23",
    "p24",
    "p25",
    "p26",
    "p27",
    "p28",
    "p29",
    "p3",
    "p4",
    "p5",
    "p6",
    "p7",
    "p8",
    "p9",
    "pa10",
    "pb",
    "pc",
    "pd",
    "pe",
    "pg",
    "ph3.5",
    "pl40",
    "pm10",
    "pn",
    "pne",
    "pnl",
    "pr40",
    "ps",
    "pw3",
    "w1",
    "w10",
    "w11",
    "w12",
    "w13",
    "w14",
    "w15",
    "w16",
    "w17",
    "w18",
    "w19",
    "w2",
    "w20",
    "w21",
    "w22",
    "w23",
    "w24",
    "w25",
    "w26",
    "w27",
    "w28",
    "w29",
    "w3",
    "w30",
    "w31",
    "w32",
    "w33",
    "w34",
    "w35",
    "w36",
    "w37",
    "w38",
    "w39",
    "w4",
    "w40",
    "w41",
    "w42",
    "w43",
    "w44",
    "w45",
    "w46",
    "w47",
    "w48",
    "w49",
    "w5",
    "w50",
    "w51",
    "w52",
    "w53",
    "w54",
    "w55",
    "w56",
    "w57",
    "w58",
    "w59",
    "w6",
    "w60",
    "w61",
    "w62",
    "w63",
    "w64",
    "w65",
    "w66",
    "w67",
    "w7",
    "w8",
    "w9", ]


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_set, image_id):
    print("executing annotation conversion")

    in_file = open('VOC2007/Annotations/%s.xml' % (image_id))
    out_file = open('VOC2007/labels/%s.txt' % (image_id), 'w')
    out_file2 = open('VOC2007/labels/%s/%s.txt' % (image_set, image_id), 'w')

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        # FIXME:
        if cls not in classes or int(difficult) == 1:
            continue

        cls_id = classes.index(cls)
        print(f'cls_id : {cls_id} ')

        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        print(f'b : {b}')
        bb = convert((w, h), b)

        out_file.write(str(cls_id) + " " +
                       " ".join([str(a) for a in bb]) + '\n')

        out_file2.write(str(cls_id) + " " +
                        " ".join([str(a) for a in bb]) + '\n')


wd = getcwd()
print(wd)

for image_set in sets:
    # 不存在就创建
    if not os.path.exists('VOC2007/labels/'):
        os.makedirs('VOC2007/labels/')

    # 不存在就创建（train/test/val)
    if not os.path.exists(f'VOC2007/labels/{image_set}'):
        os.makedirs(f'VOC2007/labels/{image_set}')

    image_ids = open('VOC2007/ImageSets/Main/%s.txt' %
                     (image_set)).read().strip().split()

    list_file = open('VOC2007/%s.txt' % (image_set), 'w')

    for image_id in image_ids:
        # list_file.write('J:/VOCdevkit/VOC2007/JPEGImages/%s/%s.jpg\n' %
        #                 (image_set, image_id))

        # 建议用绝对directory
        list_file.write('J:/VOCdevkit/VOC2007/images/%s2007/%s.jpg\n' %
                        (image_set, image_id))

        convert_annotation(image_set, image_id)
        print(f'image_set : {image_set}')
        print(f'image_id : {image_id}')
    list_file.close()
