import argparse
import collections
import os

import numpy as np
import cv2

from pycocotools.coco import COCO


def get_annotation_list(coco_dir):
    '''
    return : annotations = dict[image_path][n],
             image_list = annotations.keys()
    '''
    image_list = []
    annotations = collections.OrderedDict()

    coco = COCO(os.path.join(coco_dir, 'annotations', 'annotations.json'))
    image_ids = coco.getImgIds()
    for id in image_ids:
        annotation_ids = coco.getAnnIds(imgIds=id)

        if len(annotation_ids) == 0:
            continue

        image_info = coco.loadImgs(id)[0]
        image_path = os.path.join(coco_dir, 'images', image_info['file_name'])
        image_list.append(image_path)

        coco_annotations = coco.loadAnns(annotation_ids)

        for i, anno in enumerate(coco_annotations):
            x1 = anno['bbox'][0]
            y1 = anno['bbox'][1]
            x2 = anno['bbox'][0] + anno['bbox'][2]
            y2 = anno['bbox'][1] + anno['bbox'][3]
            class_name = coco.loadCats(anno["category_id"])[0]['name']

            if image_path not in annotations:
                annotations[image_path] = []

            annotations[image_path].append({'x1': int(x1),
                                            'y1': int(y1),
                                            'x2': int(x2),
                                            'y2': int(y2),
                                            'class': class_name})

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

        cv2.namedWindow(image_path, cv2.WINDOW_NORMAL)
        cv2.imshow(image_path, image)

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


def save_annotation_image(image_list, annotations, dir_path):
    os.makedirs(dir_path, exist_ok=True)
    for image_path in image_list:
        image = cv2.imread(image_path)
        annotation = annotations[image_path]
        if len(annotation) > 0:
            for anno in annotation:
                box = (anno['x1'], anno['y1'], anno['x2'], anno['y2'])
                draw_annotation(image, box, caption=anno['class'])
        print(make_save_image_path(dir_path, image_path))
        cv2.imwrite(make_save_image_path(dir_path, image_path), image)


def make_save_image_path(dir_path, image_path):
    image_name = os.path.basename(image_path)
    base, ext = os.path.splitext(image_name)
    new_image_name = base + '_anno' + ext
    return os.path.join(dir_path, new_image_name)


def arg_parser():
    """ Parse the arguments.
    """
    parser = argparse.ArgumentParser(description='annotation tool')
    parser.add_argument('coco', help='coco dir')
    parser.add_argument('-s', '--save',
                        help='save image annotation path',
                        default=False)
    return parser.parse_args()


def count_anno_num(annotations):
    count = 0
    for anno in annotations.values():
        count += len(anno)
    return count


def main():
    args = arg_parser()
    pwd = os.getcwd()

    annotations, image_list = get_annotation_list(args.coco)

    print('All anno num : {}\n'
          'Image num    : {}'
          .format(count_anno_num(annotations), len(image_list)))

    if args.save:
        save_dir = os.path.join(pwd, args.save)
        save_annotation_image(image_list, annotations, save_dir)
    gui(image_list, annotations)


if __name__ == "__main__":
    main()
