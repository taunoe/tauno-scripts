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


def main(argv):
    parser = argparse.ArgumentParser()

    # Required arguments
    parser.add_argument("input", help="Path to input folder")  
    parser.add_argument("output", help="Path to output folder")
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
    print("Output = {}".format(args.output))

    
if __name__ == "__main__":
  main(sys.argv)
