import BAC0,time,random
from BAC0.core.devices.local.models import (
    analog_output,
    analog_value,
    binary_value
    )

from BAC0.tasks.RecurringTask import RecurringTask 
from bacpypes.primitivedata import Real

import threading
import sys
import cv2
import time
import schedule
import requests


# create discoverable analog output of the people occ value
_new_objects = analog_value(
        name="People-Count",
        properties={"units": "noUnits"},
        description="Number of people detected from computer vision",
        presentValue=0,is_commandable=False
    )


# create bacnet app
#bacnet = BAC0.lite(ip='10.0.2.20/24',deviceId='2021')
bacnet = BAC0.lite()
  
_new_objects.add_objects_to_application(bacnet)
bacnet._log.info("APP Created Success!")

# update BACnet api on skip frame count
def update_bacnet_api(faces):
    print(f"update_bacnet_api: {faces}")
    occ_count = bacnet.this_application.get_object_name("People-Count")
    occ_count.presentValue = Real(faces)
    print(f"People-Count is {occ_count.presentValue}")



cascasdepath = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascasdepath)
video_capture = cv2.VideoCapture(0)


num_faces = None
totalFrames = 0
skip_frames = 20


try:
    while True:

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

        # update BACnet app
        if totalFrames % skip_frames == 0:
            update_bacnet_api(num_faces)
            
        
        totalFrames += 1

    video_capture.release()
    cv2.destroyAllWindows()


except KeyboardInterrupt:
    print('trying to exit gracefully')
    bacnet.disconnect()
    video_capture.release()
    cv2.destroyAllWindows()






