import argparse
import os


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

    return args


def filter_data(args):
    path_to_images, path_to_labels, path_to_incorrect_data = args


def loop(args):
    path_to_images, path_to_labels, path_to_incorrect_data = args


def main():
    args = init()
    args = check_args(args)
    #filter_data(args)
    #loop(args)


if __name__ == '__main__':
    main()
