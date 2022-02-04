#!/usr/bin/python
# https://github.com/shantnu/PyEng/blob/master/Image_Video/webcam_face_detect.py
# https://pypi.org/project/schedule/

import threading
import sys
import cv2
import time
import schedule
import requests


def job(faces):
    print("JOB running: {faces}")




cascasdepath = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascasdepath)
video_capture = cv2.VideoCapture(0)


num_faces = 0
schedule.every(30).seconds.do(job, faces=num_faces)


try:
    while True:
        schedule.run_pending()

        ret, image = video_capture.read()
        if not ret:
            break

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (30,30)
            )

        print("The number of faces found = ", len(faces))
        num_faces = len(faces)

        for (x,y,w,h) in faces:
            cv2.rectangle(image, (x,y), (x+h, y+h), (0, 255, 0), 2)

        cv2.imshow("Faces found", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


except KeyboardInterrupt:
    print('trying to exit gracefully')
    video_capture.release()
    cv2.destroyAllWindows()




'''
def run_threaded(job_func, faces):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()
'''
