import cv2
import time

from yolo_detection import detect_crowds
from utils import config
import utils


def main():
    utils.logging.info("starting program")
    try:
        for frame_counter in range(config["number_of_frames"]):

            frame, ret = utils.fetch_frame(config["frame_source"], config["max_tries"])
            if not ret:
                max_tries = config["max_tries"]
                utils.logging.warning(f"failed at fetching frames, tried {max_tries} times")
                break

            marked_frame, report = detect_crowds(frame)
            
            frame_filename = config["filename"].format(frame_counter)
            utils.update_report({frame_filename: report})
            
            frame_filepath = utils.file_path.format(frame_counter)
            cv2.imwrite(frame_filepath, marked_frame)

            number_of_frames = config["number_of_frames"]
            utils.logging.info(f"frame {frame_counter + 1}/{number_of_frames} saved with success")

            time.sleep(config["fetch_interval"])

    except KeyboardInterrupt:
        utils.logging.info("KeyboardInterrupt exception, aborting")
        exit()

if __name__ == "__main__": 
    main()
    