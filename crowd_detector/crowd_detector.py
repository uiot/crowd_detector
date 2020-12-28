'''
## passos
1. pegar todos os retangulos
2. dividi-los em aglomerados e nao aglomerados
3. desenhar-los com suas respectivas cores
4. desenhar uma linha ligando cada aglomerado
5. levantar relatorio
    - numero de pessoas detectadas
    - numero de aglomerados
'''
import cv2
import numpy as np
import logging


red = [0,0,255]
green = [0,255,0]
thickness = 10


def classify_and_draw(frame,detection_rectangles):
    '''recebe uma lista de todos os retangulos detectados e
    retorna o frame desenha, uma lista com os retangulos aglomerado
    e uma lista dos nao aglomerados
    '''
    pass


def detect_people(frame):
    '''recebe um frame e retorna uma lista
    com todos os retangulos detectados
    '''
    return []


def detect_crowds(frame):
    result_frame = frame.copy()

    people_rectangles = detect_people(frame)
    crowded_rects,_ = classify_and_draw(result_frame,people_rectangles)

    report = {
        "total detections": len(people_rectangles),
        "crowded detection": len(crowded_rects)
    }

    return result_frame, report


def test():
    frame_source = "http://208.139.200.133//mjpg/video.mjpg"
    log_level = "debug"
    logging.basicConfig(
        level=log_level.upper(),
        format='[%(levelname)s] %(asctime)s : "%(message)s"',
    )

    logging.info("starting crowd_detector test")
    logging.info("press CTRL C to exit")
    try: 
        while True:
            cap = cv2.VideoCapture(frame_source)
            ret, frame = cap.read()

            if not ret:
                logging.warning("failed to read frame")
                break

            result_frame = frame.copy()
            ##### TEST AREA #####
            
            
            cv2.rectangle(result_frame,(50,50),(200,300),(250,0,0),15)
            cv2.rectangle(result_frame,(250,300),(450,400),(250,0,0),15)
            cv2.line(result_frame, (100,150), (300,680), [0,250,0],5)
            cv2.line(result_frame, (125,175), (350,350), [0,250,0],5)
            

            # TODO: log the report
            #####################

            cv2.imwrite("test_frame.jpg",result_frame)

            logging.info("type ENTER to continue")
            input()

    except KeyboardInterrupt:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    test()
