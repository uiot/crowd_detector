import cv2
import os
import logging
import time

# from detector_utils import detect_crowds
from yolo_detection import crowd_detect as detect_crowds


def fetch_frame(source,max_tries=3):
    ret = False
    tries = 0

    while not ret and tries < max_tries:
        cap = cv2.VideoCapture(source)
        ret,frame = cap.read()
        
        tries += 1
    
    cap.release()
    return frame,ret


DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# settgings
number_of_frames = 210
fetch_interval = 3
max_tries = 3

frame_source = "http://208.139.200.133//mjpg/video.mjpg"

filename = "crowd{}.jpg"
foldername = "result_images"

log_level = "debug"

# setup
folder_path = os.path.join(DIR_PATH,foldername)
file_path = os.path.join(folder_path,filename)

try:
    os.mkdir(folder_path)
except FileExistsError:
    pass

logging.basicConfig(
    level=log_level.upper(),
    format='[%(levelname)s] %(asctime)s : "%(message)s"',
)


# main
logging.info("starting program")
logging.debug(f"estimated execution time: {(number_of_frames-1)*fetch_interval} seconds")
try:

    frame_counter = 0
    while frame_counter < number_of_frames:

        frame, ret = fetch_frame(frame_source,max_tries)
        if not ret:
            logging.warning(f"failed at fetching frames, tried {max_tries} times")
            break

        _,marked_frame = detect_crowds(frame)

        cv2.imwrite(file_path.format(frame_counter),marked_frame)
        logging.info(f"frame {frame_counter+1}/{number_of_frames} saved with success")

        frame_counter += 1
        failure_counter = 0

        time.sleep(fetch_interval)

except KeyboardInterrupt:
    logging.info("KeyboardInterrupt exception, aborting")
    exit()
