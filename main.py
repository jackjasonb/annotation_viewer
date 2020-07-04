import argparse
import collections
import numpy as np
import csv
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


def get_image_list(path):
    '''
    return : dict[image_path][n] = annotation
    '''
    csv = csv_to_list(path)
    result = collections.OrderedDict()
    for row in csv:
        img_path, x1, y1, x2, y2, class_name = row[:6]
        result[img_path].append({'x1': x1,
                                 'y1': y1,
                                 'x2': x2,
                                 'y2': y2,
                                 'class': class_name})
    return result


def draw_annotation(image, box, caption, thickness=2, color=(0, 255, 0)):
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


def main():
    args = arg_parser()
    images = get_image_list(args.anno_file)


if __name__ == "__main__":
    main()
