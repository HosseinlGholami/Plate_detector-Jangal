# plate Detection 

This repository contains a method to detect **Iranian vehicle license plates** as a representation of vehicle presence in an image. We have utilized **You Only Look Once version 3 (YOLO v.3)** to detect the plates inside an input image. The method has the advantages of high accuracy and real-time performance, thanks to YOLO v.3 architecture. The presented system receives a series of vehicle images and produces the processed image with added bounding-boxes containing the vehicles' license plates. The flow of how we have trained and tested the application is published in a paper accessible from the citation section.

## 💡 How to employ?

Test on a single image:

```
python object_detection_yolo.py --image=bird.jpg
```

Test on a single video file:

```
python object_detection_yolo.py --video=cars.mp4
```

Test on the webcam:

```
python object_detection_yolo.py
```
