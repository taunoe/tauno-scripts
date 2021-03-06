#!/usr/bin/env python3
'''
13.08.2020
Tauno Erik

Convert *.png to *.jpg:
    $ python3 ./png-to-jpg.py
Convert *.png to *.jpg and remove *.png:
'''

from PIL import Image
import glob
import os, sys
import argparse # https://docs.python.org/3.7/library/argparse.html#module-argparse
                # https://docs.python.org/3.7/howto/argparse.html#id1

def png_to_jpg():
    print("Converting *.png to *.jpg")
    for file in glob.glob("*.png"):
        im = Image.open(file)
        rgb_im = im.convert('RGB')
        rgb_im.save(file.replace("png", "jpg"), quality=95)

def remove_png():
    for file in glob.glob("*.png"):
        os.remove(file)

def main(argv):
    # commandline argument parser
    parser = argparse.ArgumentParser()

    # Required arguments
    #parser.add_argument("input", help="Path to input folder")  

    # Optional arguments
    parser.add_argument("-r","--remove", help="Remove png", action="store_true")

    args = parser.parse_args()

    png_to_jpg()

    if args.remove:
        print("Remove *.png files")
        remove_png()

if __name__ == "__main__":
    main(sys.argv)


# Requirements automatically generated by pigar.
# https://github.com/damnever/pigar