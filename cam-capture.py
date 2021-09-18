#!/usr/bin/env python3
"""
Continous Image Capture

Displays image preview on screen.
Counts down and saves image.
Restarts count down.
To exit press "q".

Started: 06.09.2021 Tauno Erik
"""

import cv2
import numpy as np
import time

"""
# Camera resolutions:
320x240
640x480
1280x720
1920x1080
"""

#### Config:
FILE_NUM = 0
SAVE_PATH = "./"                    # Save images to current directory
EXTENSION = ".png"                  # Extension for image file
CAM_WIDTH = 1280                    # Set camera width
CAM_HEIGHT = 720                    # Set camera height
SECONDS_TO_COUNTDOWN = 5            # Seconds
CROP_IMAGE = False                  # Set False to not crop and rezise images
CROPE_SIZE = 98                     # px
REZISE_SIZE = (96,96)               # px
TEXT_COLOR = (0, 0, 255)            # (B, G, R)
TEXT_FONT = cv2.FONT_HERSHEY_DUPLEX #
TEXT_SCALE = 4                      #
TEXT_THICKNESS = 4                  #


def get_webcams():
    """
    Return list of webcams
    """
    port_ids = []
    for port in range(5):
        print("Looking for a camera in port %s:" %port)

        camera = cv2.VideoCapture(port)

        if camera.isOpened():
            ret = camera.read()[0]
            if ret:
                backendName = camera.getBackendName()
                w = camera.get(3)
                h = camera.get(4)
                print("Camera {} ({} x {}) found in port {} ".format(backendName,h,w, port))
                port_ids.append(port)
            camera.release()
    return port_ids


def file_exists(filepath):
    """
    Returns true if file exists, false otherwise.
    """
    try:
        f = open(filepath, 'r')
        exists = True
        f.close()
    except:
        exists = False
    return exists


def get_filepath():
    """
    Returns the next available full path to image file
    """
    global FILE_NUM
    # Loop through possible file numbers to see if that file already exists
    filepath = SAVE_PATH + str(FILE_NUM) + EXTENSION
    while file_exists(filepath):
        FILE_NUM += 1
        filepath = SAVE_PATH + str(FILE_NUM) + EXTENSION

    return filepath


def select_camera():
    """
    Returns camera id
    """
    cam_list = get_webcams()
    if len(cam_list) == 0:
        raise Exception('Cannot find any webcameras!')
    elif len(cam_list) == 1:
        cam_id = int(cam_list[0])
    # If more than 1 camera
    elif len(cam_list) > 1:
        print("Select camera:")
        # Print avaible cameras:
        for id in cam_list:
            cam = cv2.VideoCapture(id)
            if cam.isOpened():
                ret = cam.read()[0]
                if ret:
                    cam_name = cam.getBackendName()
                    cam_w = cam.get(3)
                    cam_h = cam.get(4)
                    print("{} - Camera:{} {}x{}".format(id, cam_name, cam_h, cam_w))
                cam.release()

        cam_id = input("Enter camera number: ")
        cam_id = int(cam_id)
    return cam_id

def copy_frame(frame):
    """
    Returns cropped and resized image
    """
    # Get frame resolution
    frame_height = frame.shape[0]
    frame_width = frame.shape[1]
    # Crop center of image
    new_size = CROPE_SIZE
    start_y = int(frame_height/2 - new_size/2)
    end_y = int(frame_height/2 + new_size/2)
    start_x = int(frame_width/2 - new_size/2)
    end_x = int(frame_width/2 + new_size/2)
    # Crop
    cropped = frame[start_y:end_y, start_x:end_x]
    # Rezise
    resized = cv2.resize(cropped, REZISE_SIZE, interpolation=cv2.INTER_CUBIC)
    return resized


def main():
    # Init countdown value
    countdown = SECONDS_TO_COUNTDOWN + 1
    text = str(countdown)
    # Init: save image only when countdown = 0
    save_image = False

    # Figure out the name of the output image filename
    filepath = get_filepath()

    # Select webcameras
    cam_id= select_camera()
    cam = cv2.VideoCapture(cam_id)

    # Set camera resolution
    cam.set(3, CAM_WIDTH)
    cam.set(4, CAM_HEIGHT)

    # Initial countdown timestamp
    countdown_timestamp = cv2.getTickCount()

    while cam.isOpened():
        # Capture frame from camera
        ret, frame = cam.read()

        # Get timestamp for calculating actual framerate
        timestamp = cv2.getTickCount()

        # Each second, decrement countdown
        if (timestamp - countdown_timestamp) / cv2.getTickFrequency() > 1.0:
            countdown_timestamp = cv2.getTickCount()
            countdown -= 1
            text = str(countdown)
            
        # When countdown reaches 0
        if countdown == 0:
            # Get new image file name
            filepath = get_filepath()
            # Save image bool
            save_image = True
            # Start new count down
            countdown = SECONDS_TO_COUNTDOWN + 1
            text = "Save"

        if CROP_IMAGE:
            resized = copy_frame(frame)
            copy = resized.copy()  # Put text only on copied image
        else:
            copy = frame.copy()

        # Save image file
        if save_image:
            if CROP_IMAGE:
                # Save croped and rezised image
                cv2.imwrite(filepath, resized)
            else:
                # Save orig size image
                cv2.imwrite(filepath, frame)
            save_image = False

        text_location = (round(copy.shape[1] / 2) - 15, round(copy.shape[0] / 2)+10)

        # Draw countdown TEXT on screen image
        cv2.putText(copy, # Image
                    text, # Text
                    text_location, # org
                    TEXT_FONT,
                    TEXT_SCALE,
                    TEXT_COLOR,
                    TEXT_THICKNESS
                    )

        # Display image on screen
        cv2.imshow('Webcamera', copy)

        # Press 'q' to exit
        if cv2.waitKey(10) == ord('q'):
            break

    # Clean up
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print('To exit press "q"')
    main()
    #get_webcams()
