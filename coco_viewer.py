import argparse
import collections
import os

from pycocotools.coco import COCO

from utils import gui,  save_annotation_image


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


def count_anno_num(annotations):
    count = 0
    for anno in annotations.values():
        count += len(anno)
    return count


def arg_parser():
    """ Parse the arguments.
    """
    parser = argparse.ArgumentParser(description='annotation tool')
    parser.add_argument('coco', help='coco dir')
    parser.add_argument('-s', '--save',
                        help='save image annotation path',
                        default=False)
    return parser.parse_args()


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
