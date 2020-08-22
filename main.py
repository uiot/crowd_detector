import cv2
from yolo_detection import crowd_detect as detect
#from yolo_detection import detect


cap = cv2.VideoCapture("http://208.139.200.133//mjpg/video.mjpg")
#cap = cv2.VideoCapture(0)

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
    