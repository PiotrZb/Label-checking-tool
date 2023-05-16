import argparse
import os
import shutil
import cv2 as cv
import random
import sys

# consts
DISPLAYED_SIZE = (1280, 736)
IMAGE_FORMAT = '.png'
LABEL_FILE_FORMAT = '.txt'


def init():
    """
    Sets script args (path to images, path to labels, path to incorrect data folder).
    :return: Namespace that contains entered paths.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-ip', '--imagespath', default='./', help='Path to images')
    parser.add_argument('-lp', '--labelspath', default='./', help='Path to labels')
    parser.add_argument('-icp', '--incorrectpath', default='./IncorrectData/',
                        help='Path to folder, where incorrect data should be stored')

    return parser.parse_args()


def check_args(args):
    """
    Checks if entered paths ara valid.
    :param args: Namespace with entered paths.
    :return: tuple of three strings that represents: path to images, path to labels, path to incorrect data folder.
    """

    if not os.path.exists(args.imagespath):
        print('Path to images is invalid')
        sys.exit()

    if not os.path.exists(args.labelspath):
        print('Path to labels is invalid')
        sys.exit()

    try:
        os.makedirs(os.path.dirname(args.incorrectpath), exist_ok=True)
    except:
        print('Path to incorrect data folder is invalid')
        sys.exit()

    return (args.imagespath, args.labelspath, args.incorrectpath)


def filter_data(args):
    """
    Moves images without labels and labels without images to incorrect data folder.
    :param args: tuple of three strings that represents: path to images, path to labels, path to incorrect data folder.
    """

    path_to_images, path_to_labels, path_to_incorrect_data = args

    img_names = [x.split('.')[0] for x in os.listdir(path_to_images) if IMAGE_FORMAT in x]
    label_names = [x.split('.')[0] for x in os.listdir(path_to_labels) if LABEL_FILE_FORMAT in x]

    for img_name in img_names:
        if img_name not in label_names:
            file_name = img_name + IMAGE_FORMAT
            shutil.move(path_to_images + file_name, path_to_incorrect_data + file_name)

    for label_name in label_names:
        if label_name not in img_names:
            file_name = label_name + LABEL_FILE_FORMAT
            shutil.move(path_to_labels + file_name, path_to_incorrect_data + file_name)


def random_color():
    """
    Generates random color.
    :return: tuple of three values from 0 to 255.
    """

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return r, g, b


def draw_label(lines, img):
    """
    Draws bboxes on selected image.
    :param lines: array of strings each containing following information: id centerx centery width height.
    :param img: selected image.
    :return: image with bboxes.
    """

    img_height, img_width = img.shape[:2]

    random_color()

    for line in lines:
        id, x, y, w, h = line.split(' ')

        rect_center_x = float(x) * img_width
        rect_center_y = float(y) * img_height
        rect_width = float(w) * img_width
        rect_height = float(h) * img_height

        top_left = (int(rect_center_x - rect_width / 2), int(rect_center_y - rect_height / 2))
        bottom_right = (int(rect_center_x + rect_width / 2), int(rect_center_y + rect_height / 2))

        color = random_color()

        img = cv.rectangle(img, top_left, bottom_right, color, 2)

    return img


def loop(args):
    '''
    Loops through all images and displays them with their labels.
    Key bindings:
    * 'q' -> quit
    * 'a' -> previous
    * 'd' -> next
    * 'space' -> move to incorrect data folder
    :param args: tuple of three strings: path to images, path to labels, path to incorrect data folder.
    '''

    path_to_images, path_to_labels, path_to_incorrect_data = args

    names = [x.split('.')[0] for x in os.listdir(path_to_images) if IMAGE_FORMAT in x]

    index = 0

    while len(names) > 0:
        image = cv.imread(path_to_images + names[index] + IMAGE_FORMAT)

        # reading labels from txt
        with open(path_to_labels + names[index] + LABEL_FILE_FORMAT, 'r') as file:
            lines = file.readlines()

        image = draw_label(lines, image)
        image = cv.resize(image, DISPLAYED_SIZE)
        cv.imshow('Img', image)

        key = cv.waitKey(0)

        # quit
        if key == ord('q'):
            break

        # previous
        elif key == ord('a'):
            if index > 0:
                index -= 1

        # next
        elif key == ord('d'):
            if index < len(names) - 1:
                index += 1

        # move to IncorrectData folder
        elif key == ord(' '):
            # move images and labels to incorrect data folder
            shutil.move(path_to_images + names[index] + IMAGE_FORMAT,
                        path_to_incorrect_data + names[index] + IMAGE_FORMAT)
            shutil.move(path_to_labels + names[index] + LABEL_FILE_FORMAT,
                        path_to_incorrect_data + names[index] + LABEL_FILE_FORMAT)
            names.remove(names[index])

            if index > 0:
                index -= 1

    cv.destroyAllWindows()


def main():
    args = init()
    args = check_args(args)
    filter_data(args)
    loop(args)


if __name__ == '__main__':
    main()
