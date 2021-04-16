import numpy as np
import cv2
import itertools as it
import math
import os


DIR_PATH = os.path.dirname(os.path.realpath(__file__))

CFG_PATH = os.path.join(DIR_PATH, "yolo_files", "yolo.cfg")
CLASSES_PATH = os.path.join(DIR_PATH, "yolo_files", "yolo_classes.txt") 
WEIGHTS_PATH = os.path.join(DIR_PATH, "yolo_files", "yolo.weights")

SCALE = 0.00392
CONF_THRESHOLD = 0.4
NMS_THRESHOLD = 0.5

IGNORE_CLASSES = (
    "teddy bear",
    "donut",
)

threshold = 45


# read classes
classes = []
with open(CLASSES_PATH, 'r') as f:
    classes = [line.strip() for line in f.readlines() if not line.startswith("#")]
ignored_class_ids = [classes.index(ignored_class) for ignored_class in IGNORE_CLASSES if ignored_class in classes]

# get random colors
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

# setup net
net = cv2.dnn.readNet(WEIGHTS_PATH, CFG_PATH)

# def detect(image, *, debug=False):
def detect(image, *, debug=True):
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

    #o True espelha o RGB -----> BGR
    blob = cv2.dnn.blobFromImage(image, SCALE, (416,416), (0,0,0), True, crop=False)

    #inicia a rede neural
    net.setInput(blob)

    #processa a imagem na rede neural
    outs = net.forward(__get_output_layers(net))

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            if class_id != 0:
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

    #basicamente o que essa parte faz é remover as caixas repetidas
    #para que não haja problemas na hora de fazer reconhecimento de aglomerações

    #função para capturar o endereço de cada caixa repetida
    N = len(boxes)
    boxes_index = []
    boxes_index = [i for i in range (N)]
    pop_index = []
    for a0,a1 in it.combinations(boxes_index,2):
        if isTooClose(boxes[a0],boxes[a1]):
            if a1 not in pop_index:
                pop_index.append(a1)

    #ordena o vetor em ordem decrescente
    pop_index.sort(reverse=True)

    #remove cada caixa que foi tida como repetida
    for i in range(len(pop_index)):
        aux = pop_index[i]
        boxes.pop(aux)
    
    #NON-MAX Supression sem utilidade no momento, já que ele apenas escondia as caixas repetidas,
    #sem de fato apagá-las
    
    '''
    #aplica non-max supression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONF_THRESHOLD, NMS_THRESHOLD)
    has_detected = bool(len(indices))

    all_boxes=[]
    type (indices)
    for i in indices:
        i = i[0]
        box = boxes[i]
        all_boxes.append(box)
        
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]

        label = str(classes[class_ids[i]])

        color = COLORS[class_ids[i]]

        #cv2.rectangle(image, (round(x),round(y)), (round(x+w),round(y+h)), color, 2)
    '''
    
    #criação dos vetores que receberão as as caixas que estão perto ou longe
    dist_boxes = []
    close_boxes = []

    dist_color = (0,255,0) #BLUE, GREEN, RED - NESTE CASO VERDE PRA PESSOAS ISOLADAS
    close_color = (0,0,255) #BLUE, GREEN, RED - NESTE CASO VERMELHO PRA PESSOAS PRÓXIMAS

    #caso não haja nenhuma caixa
    if len(boxes) == 0:
        report = {}
        return image, report
    
    #caso haja apenas uma caixa
    if len(boxes) == 1:
        for b in boxes:
            cv2.rectangle(image, (round(b[0]), round(b[1])), (round(b[0]+b[2]), round(b[1]+b[3])), dist_color,3)

    #linha de referencial (no momento, sem muita utilidade)
    image = cv2.line(image, (100,100), (100,100+threshold), dist_color,3) 

    #define quais caixas estão próximas ou estão isoladas e as aloca nos seus devidos vetores
    for b0,b1 in it.combinations(boxes,2):
        if isClose(b0,b1):
            c0 =get_box_center(b0)
            c1 = get_box_center(b1)
            #print(c0,c1)
            image = cv2.line(image, c0, c1, close_color,3) 
            close_boxes.append(b0)
            close_boxes.append(b1)
        else:
            dist_boxes.append(b0)
            dist_boxes.append(b1)

   #pinta as caixas verdes para caixas isoladas ou veremelho para caixas aglomeradas
    for b in close_boxes:
        cv2.rectangle(image, (round(b[0]), round(b[1])), (round(b[0]+b[2]), round(b[1]+b[3])), close_color,7)
    for b in dist_boxes:
        cv2.rectangle(image, (round(b[0]), round(b[1])), (round(b[0]+b[2]), round(b[1]+b[3])), dist_color,3)
    
    '''
    #código provisório pois ta acontecendo algum erro com o do marcos
    if len(boxes) == 1:
        cv2.rectangle(image, (round(x),round(y)), (round(x+w),round(y+h)), dist_color, 2)

    image = cv2.line(image, (100,100), (100,100+threshold), dist_color,3) 

    for b0,b1 in it.combinations(boxes,2):
        if isClose(b0,b1):
            c0 =get_box_center(b0)
            c1 = get_box_center(b1)
            #print(c0,c1)
            image = cv2.line(image, c0, c1, close_color,3) 
            close_boxes.append(b0)
            close_boxes.append(b1)
        else:
            dist_boxes.append(b0)
            dist_boxes.append(b1)

   
    for b in close_boxes:
        cv2.rectangle(image, (round(x),round(y)), (round(x+w),round(y+h)), close_color, 2)
    for b in dist_boxes:
        cv2.rectangle(image, (round(x),round(y)), (round(x+w),round(y+h)), dist_color, 2)
    '''
    report = {}
    return image, report


def __get_output_layers(net):
    
    layer_names = net.getLayerNames()
    
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers

def get_box_center(box):
    x_center = box[0] + box[2]/2
    y_center = box[1] + box[3]/2
    return (int(x_center),int(y_center))

def isClose(box0,box1):
    pt0 = get_box_center(box0)
    pt1 = get_box_center(box1)
    dist = math.sqrt((pt1[0] - pt0[0])**2 + (pt1[1] - pt0[1])**2)  
    return (dist <= 150)

def isTooClose(box0,box1):
    pt0 = get_box_center(box0)
    pt1 = get_box_center(box1)
    dist = math.sqrt((pt1[0] - pt0[0])**2 + (pt1[1] - pt0[1])**2)  
    return (dist <= 75)

'''
if __name__ == "__main__":
    from settings import *

    cap = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    #fourcc = cv2.cv.CV_FOURCC(*'DIVX')
    #out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
    out = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            frame = cv2.flip(frame,0)
            frame = detect(frame)
            # write the flipped frame
            out.write(frame)

            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()
'''

if __name__ == "__main__":
    from settings import *

    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("http://208.72.70.172/mjpg/1/video.mjpg")
    #s = cap.read().shape
    while True:
        ret, frame = cap.read()
        s=frame.shape
        has_detected, final_frame = detect(frame, debug=True)

        #cv2.imshow("Camera Test",final_frame)

        if ret:
            #cv2.imshow("frame", final_frame)
            resized = cv2.resize(final_frame, (round(s[1]/1.1),round(s[0]/1.1)), interpolation = cv2.INTER_AREA) 
            cv2.imshow("frame",resized)
        if not cv2.waitKey(1) == -1:
            break
    
    print()
    cv2.destroyAllWindows()
    cap.release()  
