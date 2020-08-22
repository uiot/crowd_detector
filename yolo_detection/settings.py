import os


DIR_PATH = os.path.dirname(os.path.realpath(__file__))

CFG_PATH = os.path.join(DIR_PATH, "yolo_files", "yolo.cfg")
CLASSES_PATH = os.path.join(DIR_PATH, "yolo_files", "yolo_classes.txt")
WEIGHTS_PATH = os.path.join(DIR_PATH, "yolo_files", "yolo.weights")

SCALE = 0.00392
CONF_THRESHOLD = 0.3
NMS_THRESHOLD = 0.5

IGNORE_CLASSES = (
    "teddy bear",
    "donut",
)
