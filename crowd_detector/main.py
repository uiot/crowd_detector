import cv2
import time
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

from yolo_detection import detect_crowds
from utils import config
import utils


def main():
    utils.logging.info("starting program")
    try:
        #aqui temos duas funções, uma que captura a imagem em tempo real e outra que vai salvando os quadros
        #da camera a cada alguns segundos. Basta descomentar um e comentar o outro para testa-los

        #Real Time - Precisa ser otimizado, está fazendo cerca de 1 frame a cada 3 ou 4 segundos
                
        realTime()
        
        #Capture Image Frames - Vai salvando alguns frames, até completar 210 frames salvos. Muito bom para quando
        #formos publicar as estatisticas do programa
        
        #capImgFrames()

    except KeyboardInterrupt:
        utils.logging.info("KeyboardInterrupt exception, aborting")
        exit()

def realTime():
    start_time = time.time()
    display_time = 2
    fps = 0
    cap = cv2.VideoCapture(0)        
    
    '''
    if not cap.isOpened():
        raise IOError("ERRO AO ABRIR A CAMERA")
    '''

    while True:
        frame, ret = utils.fetch_frame(config["frame_source"], config["max_tries"])
        frame = cv2.resize(frame, None, fx=1.0, fy=1.0, interpolation=cv2.INTER_AREA)
        marked_frame, report = detect_crowds(frame)
        cv2.imshow("Camera Test",marked_frame)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
        
        fps += 1
        TIME = time.time() - start_time
        if TIME > display_time:
            print("FPS:", fps/TIME)
            fps = 0
            start_time = time.time()
        
    cap.release()
    cv2.destroyAllWindows()

def capImgFrames():
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

if __name__ == "__main__": 
    main()
    