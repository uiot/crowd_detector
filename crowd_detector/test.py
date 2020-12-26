import cv2
import os
import logging

from yolo_detection import crowd_detect as detect
#from yolo_detection import detect


DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# settgings
number_of_frames = 210
fetch_interval = 10

frame_source = "http://208.139.200.133//mjpg/video.mjpg"

filename = "crowd{}.jpg"
foldername = "crowd"

log_level = "debug"

# setup
file_path = os.path.join(DIR_PATH,filename)
folder_path = os.path.join(DIR_PATH,foldername)

logging.basicConfig(
    level=log_level.upper()
)

cap = cv2.VideoCapture(frame_source)


logging.info("starting program")
while True:
    ret, frame = cap.read()
    has_detected, frame = detect(frame, debug=True)
    print(has_detected)
    if ret:
        cv2.imshow("frame", frame)
    if not cv2.waitKey(1) == -1 or not ret:
        break

cv2.destroyAllWindows()
cap.release()    
    