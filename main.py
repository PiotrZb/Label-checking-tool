import argparse
import os
import shutil
import cv2 as cv
import random


def init():
    parser = argparse.ArgumentParser()

    parser.add_argument('-ip', '--imagespath', help='Path to images')
    parser.add_argument('-lp', '--labelspath', help='Path to labels')
    parser.add_argument('-icp', '--incorrectpath', help='Path to folder, where incorrect data should be stored')

    return parser.parse_args()


def check_args(args):
    if args.imagespath is None:
        args.imagespath = './'

    if args.labelspath is None:
        args.labelspath = './'

    if args.incorrectpath is None:
        args.incorrectpath = './IncorrectData/'

    return (args.imagespath, args.labelspath, args.incorrectpath)


def filter_data(args):
    path_to_images, path_to_labels, path_to_incorrect_data = args

    img_names = [x.split('.')[0] for x in os.listdir(path_to_images) if '.png' in x]
    label_names = [x.split('.')[0] for x in os.listdir(path_to_labels) if '.txt' in x]

    os.makedirs(os.path.dirname(path_to_incorrect_data), exist_ok=True)

    for img_name in img_names:
        if img_name not in label_names:
            file_name = img_name + '.png'
            shutil.move(path_to_images + file_name, path_to_incorrect_data + file_name)

    for label_name in label_names:
        if label_name not in img_names:
            file_name = label_name + '.txt'
            shutil.move(path_to_labels + file_name, path_to_incorrect_data + file_name)


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return (r, g, b)


def draw_label(lines, img):
    img_height, img_width = img.shape[:2]

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
    path_to_images, path_to_labels, path_to_incorrect_data = args

    names = [x.split('.')[0] for x in os.listdir(path_to_images) if '.png' in x]

    index = 0

    while len(names) > 0:
        image = cv.imread(path_to_images + names[index] + '.png')

        with open(path_to_labels + names[index] + '.txt', 'r') as file:
            lines = file.readlines()

        image = draw_label(lines, image)

        cv.imshow('Img', image)

        key = cv.waitKey(0)

        if key == ord('q'):  # quit
            break

        elif key != ord('a'):  # previous
            if index > 0:
                index -= 1

        elif key != ord('d'):  # next
            if index < len(names) - 1:
                index += 1

        elif key == 32:  # move to IncorrectData folder
            shutil.move(path_to_images + names[index] + '.png', path_to_incorrect_data + names[index] + '.png')
            shutil.move(path_to_labels + names[index] + '.txt', path_to_incorrect_data + names[index] + '.txt')

    cv.destroyAllWindows()


def main():
    args = init()
    args = check_args(args)
    filter_data(args)
    loop(args)


if __name__ == '__main__':
    main()
