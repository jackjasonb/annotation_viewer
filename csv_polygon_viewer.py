import argparse
import os
import cv2
import collections
import numpy as np

from utils import csv_to_list, save_annotation_image_polygon


def get_annotation_list(csv_list, img_list):
    annotations = collections.OrderedDict()
    for i, row in enumerate(csv_list):
        _, anno = row[0], row[1:]

        if img_list[i] not in annotations:
            annotations[img_list[i]] = []

        annotations[img_list[i]].append(anno)

    return annotations


def draw_annotation(image, anno):
    points = []
    for i in range(0, len(anno)-2, 2):
        points.append([[float(anno[i]), float(anno[i+1])]])
    points = np.array(points, 'int32')
    cv2.fillConvexPoly(image, points=points, color=(0, 0, 255))


def gui(img_list, anno_list):
    leftkeys = (81, 110, 65361, 2424832)
    rightkeys = (83, 109, 65363, 2555904)

    i = 0
    while True:
        image_path = img_list[i]
        image = cv2.imread(image_path)
        mask = image.copy()
        annotation = anno_list[image_path]
        if len(annotation) > 0:
            for anno in annotation:
                draw_annotation(mask, anno)
        # maskとimageの透明度
        image = cv2.addWeighted(mask, 0.3, image, 0.7, 0)
        # windowの生成
        cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
        cv2.imshow('Image', image)

        print(
            "{}  ({}/{})\n"
            "annotation_num  ({})"
            .format(os.path.basename(image_path),
                    i + 1,
                    len(img_list),
                    len(annotation))
        )

        # 左右とq(quit)の認識
        key = cv2.waitKeyEx()
        if key in rightkeys:
            i += 1
            if i >= len(img_list):
                i = 0
        if key in leftkeys:
            i -= 1
            if i < 0:
                i = len(img_list) - 1
        if (key == ord('q')) or (key == 27):
            return False


def arg_parser():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--image', help='image dir')
    parser.add_argument('-a', '--anno', help='annotation file')
    parser.add_argument(
        '-s', '--save', help='save image with annotation', default=False)
    return parser.parse_args()


def main():
    args = arg_parser()

    csv_list = csv_to_list(args.anno)
    img_list = [os.path.join(args.image, i[0]) for i in csv_list]
    annotation_list = get_annotation_list(csv_list, img_list)
    img_list = list(set(img_list))

    print('IMAGE NUM:{} / ANNO NUM:{}'.format(len(img_list), len(csv_list)))

    if args.save:
        save_annotation_image_polygon(img_list, annotation_list, args.save)
    gui(img_list, annotation_list)


if __name__ == "__main__":
    main()
