#!/usr/bin/env python3
'''	
	rename-sequenve.py
	Pythono3 code to rename multiple files in a directory.
	Tauno Erik
	13.04.2021

	https://www.geeksforgeeks.org/rename-multiple-files-using-python/
'''

import os
import sys
import argparse


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
        
        
def rename(kataloog, uus_nimi):
    files = os.listdir(kataloog)
    sorted_files = sorted(files)

    ##kataloog = "sequence"
    count = 0
    
    #for count, filename in enumerate(sorted_files):
    for filename in sorted_files:
        dst_name = uus_nimi + str(count) + ".jpg"
        dst_dir  = kataloog + "/"
        src = kataloog + "/" + filename
        dst = dst_dir + dst_name
          
        # rename() function will
        # rename all the files
        #print("src: {}".format(src))
        #print("dst: {}".format(dst))
        os.rename(src, dst)
        count += 1
        

def main(argv):

    # commandline argument parser
    parser = argparse.ArgumentParser()
    
    # Required arguments
    parser.add_argument("input_dir", help="Path to input folder")
    parser.add_argument("new_name", help="New file name")
    
    args = parser.parse_args()
    
    print("Input dir = {}".format(args.input_dir))
    print("New name = {}".format(args.new_name))
    
    # absolute path to input folder
    path = os.getcwd() + '/' + args.input_dir + '/'
    
    if os.path.isdir(path):
        print("is a directory!")
        print("path: {}".format(path))
        rename(args.input_dir, args.new_name)
        
    elif os.path.isfile(path):
        print("is a file!")
    else:
        print("Unknown input: {}".format(path))
  
  

# Driver Code
if __name__ == '__main__':
    main(sys.argv)
    
