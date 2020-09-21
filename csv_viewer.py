import argparse
import collections
import os


from utils import gui, csv_to_list, save_annotation_image_square


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


def arg_parser():
    """ Parse the arguments.
    """
    parser = argparse.ArgumentParser(description='annotation tool')
    parser.add_argument('-a', '--anno_file', help='annotation file')
    parser.add_argument('-s', '--save',
                        help='save image annotation path',
                        default=False)
    return parser.parse_args()


def main():
    args = arg_parser()
    pwd = os.getcwd()

    csv_list = csv_to_list(args.anno_file)

    os.chdir(os.path.dirname(args.anno_file))
    annotations, image_list = get_annotation_list(csv_list)

    print('All anno num : {}\n'
          'Image num    : {}'
          .format(len(csv_list), len(image_list)))

    if args.save:
        save_dir = os.path.join(pwd, args.save)
        save_annotation_image_square(image_list, annotations, save_dir)
    gui(image_list, annotations)


if __name__ == "__main__":
    main()
