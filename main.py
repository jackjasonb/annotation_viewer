import argparse
import collections
import csv
import os

import numpy as np
import cv2


def arg_parser():
    """ Parse the arguments.
    """
    parser = argparse.ArgumentParser(description='annotation tool')
    parser.add_argument('anno_file', help='annotation file')
    parser.add_argument('-s', '--save-image',
                        help='save image annotation path',
                        default='./annotation_image')
    return parser.parse_args()


def csv_to_list(path, head=False):
    list = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        if head:
            next(reader)
        for row in reader:
            list.append(row)
    return list


def get_annotation_list(csv_list):
    '''
    return : annotations = dict[image_path][n],
             image_list = annotations.keys()
    '''
    annotations = collections.OrderedDict()
    for row in csv_list:
        img_path, x1, y1, x2, y2, class_name = row[:6]

        if img_path not in annotations:
            annotations[img_path] = []

        annotations[img_path].append({'x1': int(x1),
                                      'y1': int(y1),
                                      'x2': int(x2),
                                      'y2': int(y2),
                                      'class': class_name})
    image_list = list(annotations.keys())
    return annotations, image_list


def draw_annotation(image, box, caption="", thickness=2, color=(0, 255, 0)):
    """
    box : (x1, y1, x2, y2)
    """
    box = np.array(box).astype(int)
    cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]),
                  color, thickness, cv2.LINE_AA)  # LINE_AA=アンチエイリアス
    cv2.putText(image, caption, (box[0], box[1] - 10),
                cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), thickness)
    cv2.putText(image, caption, (box[0], box[1] - 10),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), thickness-1)


def gui(image_list, annotations):
    i = 0
    leftkeys = (81, 110, 65361, 2424832)
    rightkeys = (83, 109, 65363, 2555904)
    while True:
        image_path = image_list[i]
        image = cv2.imread(image_path)
        annotation = annotations[image_path]
        if len(annotation) > 0:
            for anno in annotation:
                box = (anno['x1'], anno['y1'], anno['x2'], anno['y2'])
                draw_annotation(image, box, caption=anno['class'])

        cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
        cv2.imshow('Image', image)

        print(
            "{}  ({}/{})\n"
            "annotation_num  ({})"
            .format(os.path.basename(image_path),
                    i + 1,
                    len(image_list),
                    len(annotation))
        )

        key = cv2.waitKeyEx()

        if key in rightkeys:
            i += 1
            if i >= len(image_list):
                i = 0
        if key in leftkeys:
            i -= 1
            if i < 0:
                i = len(image_list) - 1
        if (key == ord('q')) or (key == 27):
            return False

    return True


def main():
    args = arg_parser()

    csv_list = csv_to_list(args.anno_file)
    os.chdir(os.path.dirname(args.anno_file))
    annotations, image_list = get_annotation_list(csv_list)

    print('All anno num : {}\n'
          'Image num    : {}'
          .format(len(csv_list), len(image_list)))

    gui(image_list, annotations)


if __name__ == "__main__":
    main()
