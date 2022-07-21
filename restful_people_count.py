# To read from webcam and write back out to disk:
# py restful_people_count.py -o testing.mp4
# py restful_people_count.py -c .8 -s 60

# import the necessary packages
from pyimagesearch.centroidtracker import CentroidTracker

from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2


from flask import Flask, request, jsonify, render_template, Response
import flask
import time
import threading


class mycomputer_vision(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.netPeopleCount = 0
        self.totalFrames = 0
        self.killswitch = False

        self.classes = ["background", "aeroplane", "bicycle", "bird", "boat",
            "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
            "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
            "sofa", "train", "tvmonitor"]

        self.writer = None
        self.W = None
        self.H = None

    def kill(self):

        print("kill switch hit")
        self.killswitch = True


    def run(self):
        global framecopy, vs
        
        while self.killswitch == False:

            frame = vs.read()
            frame = imutils.resize(frame, width=400)

            if self.W is None or self.H is None:
                self.H, self.W = frame.shape[:2]

            blob = cv2.dnn.blobFromImage(frame, 1.0, (self.W, self.H), (104.0, 177.0, 123.0))
            net.setInput(blob)
            detections = net.forward()
            rects = []


            for i in range(0, detections.shape[2]):
                if detections[0, 0, i, 2] > args['confidence']:

                    idx = int(detections[0, 0, i, 1])
                    if self.classes[idx] != "person":
                        continue

                    box = detections[0, 0, i, 3:7] * np.array([self.W, self.H, self.W, self.H])
                    rects.append(box.astype("int"))

                    (startX, startY, endX, endY) = box.astype("int")
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

            objects = ct.update(rects)

            for (objectID, centroid) in objects.items():
                text = "ID {}".format(objectID)
                cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

            #cv2.imshow("Frame", frame)
                
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.killswitch = True

            
            framecopy = frame.copy() 
            self.totalFrames += 1
            fps.update()


            # update flask endpoint for people
            self.netPeopleCount = len(objects)

            
        fps.stop()
        print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

        # kill switch kill computer vision
        vs.stop()


'''
Restful Web APP SETUP BELOW
'''


app = Flask(__name__)
computer_vision = mycomputer_vision()


def gen_frames():

    global framecopy
    while True:
        if framecopy is None:
                continue

        ret, buffer = cv2.imencode('.jpg', framecopy)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 


@app.route('/people-count') 
def get_updates_count(): 
    return jsonify(computer_vision.netPeopleCount)


@app.route('/reset') 
def reset_params(): 

    computer_vision.netPeopleCount = 0
    response_obj = {'status':'success'}
    return response_obj


@app.route('/video-feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


'''
MAIN LOOP BELOW
'''


if __name__ == "__main__":

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-o",
                    "--output",
                    type=str,
                    help="path to optional output video file")

    ap.add_argument("-c",
                    "--confidence",
                    type=float,
                    default=0.4,
                    help="minimum probability to filter weak detections")

    ap.add_argument('-p',
                   '--port',
                   required=False,
                   type=int,
                   default=5000,
                   help='port number to run web app on default is 5000')

    ap.add_argument('-i',
                   '--index',
                   required=False,
                   type=int,
                   default=0,
                   help='index for open CV video feed. Default is 0.')


    args = vars(ap.parse_args())
    print('Port for the Flask App Is ' + str(args["port"]))

    model = "./mobilenet_ssd/MobileNetSSD_deploy.caffemodel" 
    prototxt = "./mobilenet_ssd/MobileNetSSD_deploy.prototxt"

    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(prototxt, model)

    print("[INFO] model loaded success...")
    print("[INFO] starting video stream...")
    vs = VideoStream(src=args["index"]).start()
    time.sleep(2.0)

    ct = CentroidTracker()
    trackers = []
    trackableObjects = {}

    fps = FPS().start()

    # start computer vision on seperate thread
    computer_vision.start()

    # start flask app    
    app.run(debug=False,
    host="0.0.0.0",
    port=args["port"],
    use_reloader=False,
    threaded=True)

# CNTRL - C to kill computer vision
computer_vision.kill()


