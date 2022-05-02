# building-automation-people-counter

This repo contains a BACnet API and rest API for people counting via computer vision methods. The idea is to run this app on a machine (current testing Windows) that has a USB web camera inside the building and have IoT or the building automation system poll for total amount of people that has walked by the camera.

### Computer Vision (CV) is based on the [pyimagesearch](https://pyimagesearch.com/2018/08/13/opencv-people-counter/) people counting tutorials. 

### Python BACnet api is built on [BAC0](https://bac0.readthedocs.io/en/latest/).

### Python web app that runs the rest API endpoint is based on [Flask](https://flask.palletsprojects.com/en/2.1.x/).


![exampleSnip](/snips/exampleSnip.PNG)

### One discoverable BACnet analog value point `People-Count` which is a totalized value of people going in and out for whom have crossed the Yellow line in the video feed.

Tested on Windows 10 due to issues trying to install `dlib` on Linux. (future development on Linux env)
Install packages with pip
```
$ pip3 install -r requirements.txt
```

On Windows with Python 3.9:
```
$ py -3.9 pip install -r requirements.txt
```

# Run either BACnet API or rest API not both.

Start rest API app by:
```
# change directory to the pyimagesearch folder 
# default is horizontal yellow line, then run

$ py -3.9 restful_people_count.py
```

There is one GET URL endpoint `http://localhost:5000/people-count` that will return a JSON response:
```
{
	"People-Count": 12
}
```

Start BACnet app by:
```
# change directory to the pyimagesearch folder 
# default is horizontal yellow line, then run

$ py -3.9 bacnet_people_counter.py
```

OPTIONAL args for vertical people crossing line
```
$ py -3.9 bacnet_people_counter.py -v True
```


#### Save a video file output in mp4 format:
`-o` which is the path to optional output video file in string format

#### Confidence for minimum probability for classification of a peron in video feed. Every `s` skipframe of the video feed a classification algorithm is ran to see if more people have entered the video feed. This arg can be tweaked to improve performance:
`-c` minimum probability to filter weak detections in float, default is 0.4.

#### Skipframe for the video feed to reclassify objects in the frame. Other frames of the video feed that are not "skipframes" object tracking algorithms are used with the `dlib` package:
`-s` this number default is 30 frames could be used for performance tuning purposes depending on the amount of people and overall frame per second (FPS) performance. 


## To stop app use `CNTRL-C` which will also print FPS and elapsed time.

```
[INFO] elapsed time: 2.85
[INFO] approx. FPS: 70.24

```

### Hopefully more testing soon!