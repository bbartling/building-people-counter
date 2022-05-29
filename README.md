# datalog-building-people-counter
This repo needs testing in real world environment, the idea is to share data to a building automation system (BAS) on a local area network (LAN). Heating, ventilation, and air conditioning (HVAC) in commercial buildings can use occupancy data to save on building fuel consumption which saves money and green house gas emmissions. 
This repo contains a BACnet API and rest API for people counting via computer vision methods. The idea is to run this app on a machine (current testing Windows) that has a USB web camera inside the building and have IoT or the building automation system poll for total amount of people that has walked by the camera.

- Computer Vision (CV) is based on the [pyimagesearch](https://pyimagesearch.com/2018/08/13/opencv-people-counter/) people counting tutorials. 
- Python web app that runs the rest API endpoint to retrieve people count metrics and to render computer vision in browser is based on [Flask](https://flask.palletsprojects.com/en/2.1.x/).


![exampleSnip](/snips/exampleSnip.PNG)


On Windows with Python 3.10:
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

$ py -3.9 restful_people_count.py
```

There is one GET URL endpoint `http://localhost:5000/people` (tested on localhost) that will return a JSON response of the object count telemetry:
```
{
	"info": {
		"count": 1,
		"in": 5,
		"out": 4
	},
	"status": "success"
}
```

Web app also includes specific endpoints to retrieve direct data values:
- `http://localhost:5000/people/count`
- `http://localhost:5000/people/in` 
- `http://localhost:5000/people/out` 


And there is another GET URL endpoint `http://localhost:5000/reset` to reset the object count telemetry back to zero. The idea would be for to connect up the `reset` endpoint to a BAS schedule or some sort of external IoT reoccuring task to reset numbers each day, like for example every day at midnight a BAS schedule triggers a GET request to `reset` parameters everynight to keep data consistant for daily record keeping purposes.


OPTIONAL args for vertical people crossing line
```
$ py -3.9 restful_people_count.py-v True
```


#### Save a video file output in mp4 format:
`-o` which is the path to optional output video file in string format

#### Confidence for minimum probability for classification of a peron in video feed. Every `s` skipframe of the video feed a classification algorithm is ran to see if more people have entered the video feed. This arg can be tweaked to improve performance:
`-c` minimum probability to filter weak detections in float, default is 0.4.

#### Skipframe for the video feed to reclassify objects in the frame. Other frames of the video feed that are not "skipframes" object tracking algorithms are used with the `dlib` package:
`-s` this number default is 30 frames could be used for performance tuning purposes depending on the amount of people and overall frame per second (FPS) performance. 


## To stop app press `q` on the camera feed window and then a `CNTRL-c` in command prompt to exit gracefully. This also will also print FPS and elapsed time.

```
[INFO] elapsed time: 2.85
[INFO] approx. FPS: 70.24

```

Hopefully more testing soon for the interception of existing IP security camera systems and possible USB camera deployment on a Nvidia Jetson Nano! Got any ideas to try submit a github discussion or issue!