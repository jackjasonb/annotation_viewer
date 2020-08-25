import os
import cv2
import numpy as np
import csv


def csv_to_list(path, head=False):
    list = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        if head:
            next(reader)
        for row in reader:
            list.append(row)
    return list


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


def make_save_image_path(dir_path, image_path):
    image_name = os.path.basename(image_path)
    base, ext = os.path.splitext(image_name)
    new_image_name = base + '_anno' + ext
    return os.path.join(dir_path, new_image_name)


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
