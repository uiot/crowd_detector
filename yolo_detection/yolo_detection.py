import numpy as np
import cv2

if __name__ != "__main__":
    from .settings import *
else:
    from settings import *

# read classes
classes = []
with open(CLASSES_PATH, 'r') as f:
    classes = [line.strip() for line in f.readlines() if not line.startswith("#")]
ignored_class_ids = [classes.index(ignored_class) for ignored_class in IGNORE_CLASSES if ignored_class in classes]

# get random colors
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

# setup net
net = cv2.dnn.readNet(WEIGHTS_PATH, CFG_PATH)

def detect(image, *, debug=False):
    """Returns True if any deteciton ocurred,
    and False otherwise.
    If debug is True, returns a second 
    variable being the input frame with
    rectangles around the detections.
    """
    class_ids = []
    confidences = []
    boxes = []

    Width = image.shape[1]
    Height = image.shape[0]

    blob = cv2.dnn.blobFromImage(image, SCALE, (416,416), (0,0,0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(__get_output_layers(net))

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            if class_id in ignored_class_ids:
                continue
            confidence = scores[class_id]
            if confidence > 0.5:
                if not debug:
                    return True
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    if not debug:
        return False

    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONF_THRESHOLD, NMS_THRESHOLD)
    has_detected = bool(len(indices))

    for i in indices:
        i = i[0]
        box = boxes[i]
        print(box)
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        __draw_prediction_and_labels(image, class_ids[i], round(x), round(y), round(x+w), round(y+h))

    return has_detected, image

def __get_output_layers(net):
    
    layer_names = net.getLayerNames()
    
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers

def __draw_prediction_and_labels(img, class_id, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

if __name__ == "__main__":
    from settings import *

    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("http://208.139.200.133//mjpg/video.mjpg")

    while True:
        ret, frame = cap.read()
        
        has_detected, final_frame = detect(frame, debug=True)

        if ret:
            cv2.imshow("frame", final_frame)
        if not cv2.waitKey(1) == -1:
            break
    
    print()
    cv2.destroyAllWindows()
    cap.release()  

