# https://syntaxfix.com/question/464/access-ip-camera-in-python-opencv

import sys
import cv2
import time
from imutils.video import FPS


cascasdepath = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascasdepath)


''' Use a "0" for built in web cam or a "1" for USB camera '''
#video_capture = cv2.VideoCapture(0)

''' IP CAMERA SETUP '''
''' "videofeed" is unique to Andriod app being tested '''
video_capture = cv2.VideoCapture('http://192.168.0.106:8080/videofeed')



#num_faces = 0
fps = FPS().start()


try:
    while True:

        ret, image = video_capture.read()
        if not ret:
            print("no video feed, breaking out of script")
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

        # counter to print FPS at the end
        fps.update()

        for (x,y,w,h) in faces:
            cv2.rectangle(image, (x,y), (x+h, y+h), (0, 255, 0), 2)

        cv2.imshow("Faces found", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    print('trying to exit gracefully')
    video_capture.release()
    cv2.destroyAllWindows()


except KeyboardInterrupt:
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    print('trying to exit gracefully')
    video_capture.release()
    cv2.destroyAllWindows()




