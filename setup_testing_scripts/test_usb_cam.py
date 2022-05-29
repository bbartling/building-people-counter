# https://stackoverflow.com/questions/62959030/how-do-i-access-my-usb-camera-using-opencv-with-python
# this script will print the camera index to try
# for use in main app --usb-index


import cv2
import numpy as np

all_camera_idx_available = []

for camera_idx in range(10):
    cap = cv2.VideoCapture(camera_idx)
    if cap.isOpened():
        print(f'Camera index available: {camera_idx}')
        all_camera_idx_available.append(camera_idx)
        cap.release()




