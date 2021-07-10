#!/bin/bash


# Install stuff
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
wget -O ./crowd_detector/yolo_detection/yolo_files/yolo.weights \
https://pjreddie.com/media/files/yolov3.weight

# Install opencv