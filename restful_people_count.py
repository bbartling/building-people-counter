# To read from webcam and write back out to disk:
# py -3.9 people_counter.py 

# import the necessary packages
from pyimagesearch.centroidtracker import CentroidTracker
from pyimagesearch.trackableobject import TrackableObject
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
        self.netCountOut = 0
        self.netCountIn = 0
        self.totalFrames = 0
        self.killswitch = False


    def kill(self):

        print("kill switch hit")
        self.killswitch = True


    def run(self):
        global framecopy, vs
        
        model = "./mobilenet_ssd/MobileNetSSD_deploy.caffemodel" 
        prototxt = "./mobilenet_ssd/MobileNetSSD_deploy.prototxt"

        # load our serialized model from disk
        print("[INFO] loading model...")
        
        # net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
        net = cv2.dnn.readNetFromCaffe(prototxt, model)

        # load our serialized model from disk
        print("[INFO] model loaded success...")



        # initialize the list of class labels MobileNet SSD was trained to
        # detect
        CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
            "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
            "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
            "sofa", "train", "tvmonitor"]



        print("[INFO] starting video stream...")
        vs = VideoStream(src=0).start()
        time.sleep(0.0)

        # initialize the video writer (we'll instantiate later if need be)
        writer = None

        # initialize the frame dimensions (we'll set them as soon as we read
        # the first frame from the video)
        W = None
        H = None

        # instantiate our centroid tracker, then initialize a list to store
        # each of our dlib correlation trackers, followed by a dictionary to
        # map each unique object ID to a TrackableObject
        ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
        trackers = []
        trackableObjects = {}


        # start the frames per second throughput estimator
        fps = FPS().start()
        
        
        def countIn():
            print("countIn()")
            self.netCountIn += 1
            netPeopleCount = self.netCountIn - self.netCountOut
            if netPeopleCount <= 0:
                netPeopleCount = 0
            to.counted = True
            self.netPeopleCount = netPeopleCount


        def countOut():
            print("countOut()")
            self.netCountOut += 1
            netPeopleCount = self.netCountIn - self.netCountOut
            if netPeopleCount <= 0:
                netPeopleCount = 0
            to.counted = True
            self.netPeopleCount = netPeopleCount


        # loop over frames from the video stream
        while self.killswitch == False:
            # grab the next frame and handle if we are reading from either
            # VideoCapture or VideoStream
            frame = vs.read()

            # resize the frame to have a maximum width of 500 pixels (the
            # less data we have, the faster we can process it), then convert
            # the frame from BGR to RGB for dlib
            frame = imutils.resize(frame, width=500)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # if the frame dimensions are empty, set them
            if W is None or H is None:
                (H, W) = frame.shape[:2]

            # if we are supposed to be writing a video to disk, initialize
            # the writer
            if args["output"] is not None and writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter(args["output"], fourcc, 30,
                    (W, H), True)

            # initialize the current status along with our list of bounding
            # box rectangles returned by either (1) our object detector or
            # (2) the correlation trackers
            status = "Waiting"
            rects = []

            # check to see if we should run a more computationally expensive
            # object detection method to aid our tracker
            if self.totalFrames % args["skip_frames"] == 0:
                # set the status and initialize our new set of object trackers
                status = "Detecting"
                trackers = []

                # convert the frame to a blob and pass the blob through the
                # network and obtain the detections
                blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
                net.setInput(blob)
                detections = net.forward()

                # loop over the detections
                for i in np.arange(0, detections.shape[2]):
                    # extract the confidence (i.e., probability) associated
                    # with the prediction
                    confidence = detections[0, 0, i, 2]

                    # filter out weak detections by requiring a minimum
                    # confidence
                    if confidence > args["confidence"]:
                        # extract the index of the class label from the
                        # detections list
                        idx = int(detections[0, 0, i, 1])

                        # if the class label is not a person, ignore it
                        if CLASSES[idx] != "person":
                            continue

                        # compute the (x, y)-coordinates of the bounding box
                        # for the object
                        box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                        (startX, startY, endX, endY) = box.astype("int")

                        # construct a dlib rectangle object from the bounding
                        # box coordinates and then start the dlib correlation
                        # tracker
                        tracker = dlib.correlation_tracker()
                        rect = dlib.rectangle(int(startX), int(startY), int(endX), int(endY))
                        tracker.start_track(rgb, rect)

                        # add the tracker to our list of trackers so we can
                        # utilize it during skip frames
                        trackers.append(tracker)

            # otherwise, we should utilize our object *trackers* rather than
            # object *detectors* to obtain a higher frame processing throughput
            else:
                # loop over the trackers
                for tracker in trackers:
                    # set the status of our system to be 'tracking' rather
                    # than 'waiting' or 'detecting'
                    status = "Tracking"

                    # update the tracker and grab the updated position
                    tracker.update(rgb)
                    pos = tracker.get_position()

                    # unpack the position object
                    startX = int(pos.left())
                    startY = int(pos.top())
                    endX = int(pos.right())
                    endY = int(pos.bottom())

                    # add the bounding box coordinates to the rectangles list
                    rects.append((startX, startY, endX, endY))

            # draw a horizontal line in the center of the frame -- once an
            # object crosses this line we will determine whether they were
            # moving 'up' or 'down'

            if not args["vertical"]:
                cv2.line(frame, (0, H // 2), (W, H // 2), (0, 255, 255), 2)
                
            else:
                cv2.line(frame, (W//2,0), (W//2, H) , (0,255,255), 2)


            # use the centroid tracker to associate the (1) old object
            # centroids with (2) the newly computed object centroids
            objects = ct.update(rects)

            # loop over the tracked objects
            for (objectID, centroid) in objects.items():
                # check to see if a trackable object exists for the current
                # object ID
                to = trackableObjects.get(objectID, None)

                # if there is no existing trackable object, create one
                if to is None:
                    to = TrackableObject(objectID, centroid)

                # otherwise, there is a trackable object so we can utilize it
                # to determine direction
                else:
                    # the difference between the y-coordinate of the *current*
                    # centroid and the mean of *previous* centroids will tell
                    # us in which direction the object is moving (negative for
                    # 'in' and positive for 'out')
                    y = [c[1] for c in to.centroids]
                    direction = centroid[1] - np.mean(y)
                    to.centroids.append(centroid)
                

                    # check to see if the object has been counted or not
                    if not to.counted:

                        print("centroid[1] IS: ",centroid[1])
                        print("W IS: ",W)
                        print("W // 2 IS: ",W // 2)
                        print("DIRECTION IS: ",direction)
                        print("centroid[1] < W // 2: ",centroid[1] < W // 2)
                    
                        # if the direction is negative (indicating the object
                        # is moving in) AND the centroid is above the center
                        # line, count the object
                        if not args["vertical"]:
                            if direction < 0 and centroid[1] < H // 2:
                                countIn()
                                to.counted = True

                        # if the direction is positive (indicating the object
                        # is moving out) AND the centroid is below the
                        # center line, count the object
                            elif direction > 0 and centroid[1] > H // 2:
                                countOut()
                                to.counted = True

                        else: # math is different with vert line for counting 
                            if direction < 0 and centroid[1] < W // 2:
                                countIn()
                                to.counted = True

                            elif direction > 0 and centroid[1] > W // 2:
                                countOut()
                                to.counted = True

                # store the trackable object in our dictionary
                trackableObjects[objectID] = to

                # draw both the ID of the object and the centroid of the
                # object on the output frame
                text = "ID {}".format(objectID)
                cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

            # construct a tuple of information we will be displaying on the
            # frame
            info = [
                ("In", self.netCountIn),
                ("Out", self.netCountOut),
                ("Status", status),
            ]

            # loop over the info tuples and draw them on our frame
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # check to see if we should write the frame to disk
            if writer is not None:
                writer.write(frame)

            # concat frame one by one and show result
            # web app
            framecopy = frame.copy() 

            # increment the total number of frames processed thus far and
            # then update the FPS counter
            self.totalFrames += 1
            fps.update()

        # stop the timer and display FPS information
        fps.stop()
        print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

        # check to see if we need to release the video writer pointer
        if writer is not None:
            writer.release()

        # kill switch kill computer vision
        vs.stop()


'''
Restful Web APP SETUP BELOW
'''


app = Flask(__name__)
computer_vision = mycomputer_vision()

# used to render computer vision in browser
def gen_frames():

    global framecopy
    while True:
        if framecopy is None:
                continue

        ret, buffer = cv2.imencode('.jpg', framecopy)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 


@app.route('/people') 
def get_updates(): 

    info = {"count":computer_vision.netPeopleCount,
            "out":computer_vision.netCountOut,
            "in":computer_vision.netCountIn}  

    response_obj = {'status':'success','info':info}
    
    return response_obj


@app.route('/people/count') 
def get_updates_count(): 
    return jsonify(computer_vision.netPeopleCount)


@app.route('/people/out') 
def get_updates_out(): 
    return jsonify(computer_vision.netCountOut)


@app.route('/people/in') 
def get_updates_in(): 
    return jsonify(computer_vision.netCountIn)


@app.route('/reset') 
def reset_params(): 

    computer_vision.netPeopleCount = 0
    computer_vision.netCountOut = 0
    computer_vision.netCountIn = 0

    response_obj = {'status':'success'}

    return response_obj



@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
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
                    default=0.9,
                    help="minimum probability to filter weak detections")

    ap.add_argument("-s",
                    "--skip-frames",
                    type=int,
                    default=60,
                    help="# of skip frames between detections")

    ap.add_argument("-v",
                    "--vertical",
                    type=bool,
                    default=False,
                    help="specify vertical or horizontal line")

    ap.add_argument('-p',
                   '--port',
                   required=False,
                   type=int,
                   default=5000,
                   help='port number to run web app on default is 5000')


    args = vars(ap.parse_args())
    print('Port for the Flask App Is ' + str(args["port"]))

    # start computer vision on seperate thread
    computer_vision.start()

    # start flask app    
    app.run(debug=True,
    host="0.0.0.0",
    port=args["port"],
    use_reloader=False,
    threaded=True)


# CNTRL - C to kill computer vision
computer_vision.kill()


