import logging
import os
import cv2
import yaml
import json


__root_path = os.path.dirname(os.path.realpath(__file__))
__config_filename = "config.yaml"

with open(os.path.join(__root_path, __config_filename)) as config_file:
    config = yaml.safe_load(config_file)

__folder_path = os.path.join(__root_path, config["foldername"])
file_path = os.path.join(__folder_path, config["filename"])

try:
    os.mkdir(__folder_path)
except FileExistsError:
    pass

logging.basicConfig(
    level=config["log_level"].upper(),
    format='[%(levelname)s] %(asctime)s : "%(message)s"',
)


def fetch_frame(source,max_tries=3):
    '''Tries to fetch one frame from the source max_tries times, and then returns it.
    '''
    for i in range(max_tries):
        logging.debug(f"entering try number {i+1}/{max_tries}")

        cap = cv2.VideoCapture(source)
        ret,frame = cap.read()
        
        if ret: break

    cap.release()
    return frame, ret

def update_report(report):
    reports_path = os.path.join(__root_path, config["reports_filename"])
    
    try:
        with open(reports_path) as reports_file:
            reports = json.load(reports_file)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        reports = {}

    reports.update(report)
    with open(reports_path,'w') as reports_file:
            json.dump(reports, reports_file, indent=4)
