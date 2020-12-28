import cv2
import numpy as np
import itertools as it
import os


DIR_PATH = os.path.dirname(os.path.realpath(__file__))

CFG_PATH = os.path.join(DIR_PATH, "yolo_files", "yolo.cfg")
WEIGHTS_PATH = os.path.join(DIR_PATH, "yolo_files", "yolo.weights")

SCALE = 0.00392
CONF_THRESHOLD = 0.3
NMS_THRESHOLD = 0.5

CLASS = "person"

GREEN = (200,200,200)
RED = (0,0,0)

net = net = cv2.dnn.readNet(WEIGHTS_PATH, CFG_PATH)


def draw_boxes(image, boxes, color):
    print(image, boxes, color)
    print
    for box in boxes:
        x = box[0]
        y = box[1]
        x_plus_w = box[0] + box[2]
        y_plus_h = box[1] + box[3]
        color =  np.random.uniform(0, 255, size=(40, 3))
        #color = np.array([0,0,0])
        #cv2.rectangle(image, (box[0],box[2]), (box[0] + box[2],box[1] + box[3]), (0,0,0))
        #cv2.rectangle(img=image, pt1=(x,y), pt2=(x_plus_w,y_plus_h), rec=1, , thickness=2)
    return image
'''
def draw_boxes(img, boxes,a):
    for box in boxes:
        x = box[0]
        y = box[1]
        x_plus_w = box[0] + box[2]
        y_plus_h = box[1] + box[3]
        COLORS = np.random.uniform(0, 255, size=(40, 3))

        color = COLORS[0]

        cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
'''

def isClose(p1, p2):
    return False

def get_box_center(box):
    x_center = box[0] + box[2]/2
    y_center = box[1] + box[3]/2
    return (x_center,y_center)

def find_all_bouding_boxes(image):
    class_ids = []
    confidences = []
    boxes = []

    Width = image.shape[1]
    Height = image.shape[0]

    blob = cv2.dnn.blobFromImage(image, SCALE, (416,416), (0,0,0), True, crop=False)
    net.setInput(blob)
    
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    outs = net.forward(output_layers)
    #print(outs)
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            if class_id != 0:
                continue
            confidence = scores[class_id]
            if confidence > 0.5:
    
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONF_THRESHOLD, NMS_THRESHOLD)

    result_boxes = list()

    for i in indices:
        i = i[0]
        box = boxes[i]
        result_boxes.append(box)
    
    return result_boxes


def detect(image):
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
            '''if class_id in ignored_class_ids:
                continue'''
            if class_id != 0:
                continue
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])


    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONF_THRESHOLD, NMS_THRESHOLD)
    result = list()
    for i in indices:
        i = i[0]
        box = boxes[i]
        result.append(box)
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
    return result

def __get_output_layers(net):
    
    layer_names = net.getLayerNames()
    
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def crowd_detection(image):
    
    #all_bouding_boxes = find_all_bouding_boxes(image)
    all_bouding_boxes = detect(image)
    print(all_bouding_boxes)
    crowded_boxes = distant_boxes = list()
    for box1, box2 in it.combinations(all_bouding_boxes, 2):
        print(box1,b)
        if isClose(box1, box2):
            crowded_boxes.append(box1)
            crowded_boxes.append(box2)
        else:
            distant_boxes.append(box1)
            distant_boxes.append(box2)

    crowd_qnt = len(crowded_boxes)
    dinstant_qnt = len(distant_boxes)

    final_image = image.copy()
    for crowded_box, distant_box in zip(crowded_boxes,distant_boxes):
        print(final_image, (distant_box[0], distant_box[1]), ((distant_box[0]+distant_box[2]), (distant_box[1]+distant_box[3])), 240, 2)
        cv2.rectangle(final_image, (crowded_box[0], crowded_box[1]), ((crowded_box[0]+crowded_box[2]), (crowded_box[1]+crowded_box[3])))
        cv2.rectangle(final_image, (distant_box[0], distant_box[1]), ((distant_box[0]+distant_box[2]), (distant_box[1]+distant_box[3])), 240, 2)

    return final_image, crowd_qnt, dinstant_qnt

    
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture("http://208.139.200.133//mjpg/video.mjpg")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("No frame")
            break
        
        final_frame, crowd_qnt, dinstant_qnt = crowd_detection(frame)
        #print("\r", "crowd_qnt = ", crowd_qnt, "dinstant_qnt = ", dinstant_qnt, end="     ")
        cv2.imshow("frame", final_frame)
        if not cv2.waitKey(1) == -1:
            break
    
    print()
    cv2.destroyAllWindows()
    cap.release()    
    