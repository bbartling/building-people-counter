# building-people-counter

(insert snip of laptop & USB cam) 

- Computer Vision (CV) is based on the [pyimagesearch](https://pyimagesearch.com/2018/08/13/opencv-people-counter/) people counting tutorials for object tracking. 
- Python web app that runs the rest API endpoint to retrieve people count metrics and to render computer vision in browser is based on [Flask](https://flask.palletsprojects.com/en/2.1.x/).


![exampleSnip](/snips/exampleSnip.PNG)


On Windows with Python 3.9 and 3.10 with 64 bit executable file:
https://www.python.org/downloads/release/python-3104/

Clone the repo and change directoy into the project
Next install Python packages with pip:

```
$ py pip install -r requirements.txt
```

Attempt to install `cmake`:
```
$ py -m pip install cmake
```

Hopefully success so far, then attempt to install `dlib` with this tutorial:
https://www.youtube.com/watch?v=-pZEDxDRyGQ

Start app by:
```
# default port is 5000, but use -p arg to specify a specific port number

$ py restful_people_count.py
```

Computer vision can be viewed in the web browser on `http://localhost:5000.` One GET URL endpoint `http://localhost:5000/people-count` (tested on localhost) that will return a JSON response of the object count representing trackable objects or people in the video frame.


#### Confidence for minimum probability for classification of a peron in video feed. Every `s` skipframe of the video feed a classification algorithm is ran to see if more people have entered the video feed. This arg can be tweaked to improve performance:
`-c` minimum probability to filter weak detections in float, default is 0.4.

## To stop app use CTRL-Q in command prompt to exit gracefully. This also will also print FPS and elapsed time.

```
kill switch hit
>>> [INFO] elapsed time: 143.96
[INFO] approx. FPS: 11.07

```

Got any ideas to try submit a github discussion or issue!