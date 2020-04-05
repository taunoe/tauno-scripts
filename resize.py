#!/usr/bin/env python3
'''
rezise.py
Tauno Erik
04.04.2020
'''

import os, sys
import argparse # https://docs.python.org/3.7/library/argparse.html#module-argparse
                # https://docs.python.org/3.7/howto/argparse.html#id1
from PIL import Image


def check_folder(new_folder):
    if os.path.isdir(new_folder) == False:
        make_folder(new_folder)
    else:
        print("Folder already exists")


def make_folder(path):
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory {} failed".format(path))
    else:
        print ("Successfully created the directory {} ".format(path))


def calculate_size(old_width, old_height, shorter_side):
    '''
    Calculates new image size
    '''
    # portrait
    if old_width < old_height: 
        new_height = int((((shorter_side * 100) / old_width) / 100) * old_height)
        return(shorter_side, new_height)
    # landscape 
    elif old_height < old_width: 
        new_width = int((((shorter_side * 100) / old_height) / 100) * old_width)
        return(new_width, shorter_side)
    # square
    else:
        return(shorter_side, shorter_side)


def convert_images(path, images, size=1024):

    # Make size named subfolder
    new_folder = path + str(size) + '/' # absolute path
    check_folder(new_folder)

    for file in images:
        
        if file.endswith('.png') or file.endswith('.jpg'):

            print("Name: {}".format(file))
            im = Image.open(path + file)

            old_width, old_height = im.size
            print("Old: {}:{}".format(old_width, old_height))

            new_width, new_height = calculate_size(old_width, old_height, size)
            print("New: {}:{}".format(new_width, new_height))

            new_im = im.resize((new_width, new_height))#.convert("RGB")
            new_im.save(new_folder + file)

def main(argv):

    # commandline argument parser
    parser = argparse.ArgumentParser()

    # Required arguments
    parser.add_argument("input", help="Path to input folder")  
    parser.add_argument("size", type=int, help="New image size")

    # Optional arguments
    parser.add_argument("-l","--logo", help="Add logo", action="store_true") 
    parser.add_argument("-t","--time", help="Add time", action="store_true")

    args = parser.parse_args()

    if args.logo:
        print("Lisan logo.")

    if args.time:
        print("Lisan kuupäeva.")

    if args.size:
        print("New size = {}".format(args.size))

    print("Input = {}".format(args.input))

    # absolute path to input images folder
    path = os.getcwd() + '/' + args.input + '/' 

    if os.path.isdir(path):
        print("is folder")
        images = os.listdir(path)
        convert_images(path, images, args.size)
    elif os.path.isfile(path):
        print("is file")
    else:
        print("Unknown input: {}".format(path))

    
if __name__ == "__main__":
  main(sys.argv)
