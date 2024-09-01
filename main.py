import cv2 as cv
import numpy as np
from utils import Utils, FixedSizeList
from time import time
from dataclasses import dataclass
from config import Config, Default
from calibrate import Calibrate
import os

def main():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # Config
    config = Config()

    user_input = ' '
    running = True
    while running:
        os.system('cls||clear')
        print(
            f"""
                +=============================================================+
                | ALINHAMENTO DE CORREIA                                      |
                +=============================================================+
                  VARIAVEIS                                                   
                     Threshold: {config.threshold};                                  
                     Multiplicador: {config.multiplier};                             
                     Intervalo para Processamento (s): {config.image_interval};      
                     Tolerância para atuador (pixels): {config.tolerance};           
                  OPCOES                                                      
                     1. Calibrar Threshold                                    
                     2. Calibrar Multiplicador                                
                     3. Teste    
                     4. Editar Intervalo p/ Processamento
                     5. Editar Tolerância para Atuador                                             
                     q. Sair                                                  
                ===============================================================
            """
        )
        user_input = input()
        if len(user_input) == 0:
            pass
        elif user_input[0] == '1':
            config.threshold = Calibrate.get_threshold(cap)
        elif user_input[0] == '2':
            original_polygon, config.multiplier = Calibrate.get_multiplier(cap, config.threshold)
        elif user_input[0] == '3':
            try:
                test(cap, original_polygon, config.threshold, config.multiplier, config.image_interval, config.tolerance)
            except UnboundLocalError:
                print('Calibre o multiplicador com a opção 2 antes!')
        elif user_input[0] == '4':
            try:
                interval = float(input('Insira o novo Intervalo (s): '))
                if interval < 0:
                    print('O intervalo deve ser positivo!')
                else:
                    config.image_interval = interval
            except Exception:
                print('Insira um float!')
        elif user_input[0] == '5':
            try:
                tolerance = float(input('Insira a nova Tolerância: '))
                if tolerance < 0:
                    print('A tolerância deve ser positiva!')
                else:
                    config.tolerance = tolerance
            except Exception:
                print('Insira um inteiro!')
            
        elif user_input[0] == 'q':
            config.save()
            os.system('cls||clear')
            running = False
    cap.release()
    cv.destroyAllWindows()
    
def test(
        cap: cv.VideoCapture, 
        original_polygon: np.array, 
        threshold: int = 127, 
        multiplier: float = 0.001, 
        image_interval: float = 1, 
        tolerance: int = 10
    ):
    ret, frame = cap.read()
    black_image = np.zeros_like(frame, dtype="uint8")
    original_filled_polygon = black_image.copy()
    cv.fillPoly(original_filled_polygon, [original_polygon], color=Default.white)
    original_polygon_area = np.sum(original_filled_polygon[:, :, 0])
    original_moment = cv.moments(original_polygon)
    original_x_centroid = int(original_moment['m10']/original_moment['m00']) 

    # Camera Dimensions
    width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

    # Areas
    live_x_centroid = width/2
    image_series = FixedSizeList(20)
    displaced_area_series = FixedSizeList(20)
    displaced_area = 0

    # Time
    previous = time()
    delta = image_interval

    main_loop = True
    while main_loop:
        ret, frame = cap.read()

        # Time
        current = time()
        delta += current - previous
        previous = current
        if delta > image_interval:
            delta = 0
            processed_image = Utils.process_image(frame, threshold)
            image_series.append(processed_image)
            image_median = image_series.get_median({'axis': 0}).astype("uint8")
            image_median = cv.medianBlur(image_median, 3)
        
        # Identify polygon around belt
        try:
            live_polygon = Utils.get_object_polygon_contour(image_median, multiplier)
            live_moment = cv.moments(live_polygon)
            live_x_centroid = int(live_moment['m10']/live_moment['m00'])
            cv.drawContours(frame, [live_polygon], -1, Default.red, 2)
            cv.line(frame, (live_x_centroid, int(height/2)), (original_x_centroid, int(height/2)), Default.blue, 2)
            live_filled_polygon = black_image.copy()
            cv.fillPoly(live_filled_polygon, [live_polygon], color=Default.white)
            displaced_area = np.sum(live_filled_polygon[:, :, 0] & original_filled_polygon[:, :, 0])
            displaced_area_series.append(displaced_area)
        except Exception as e:
            print('Nenhum contorno. Verificar', e)

        # Get correct side
        centroid_difference = original_x_centroid - live_x_centroid
        if centroid_difference > tolerance:
            actor_response = 'Esquerda'
        elif centroid_difference < -tolerance: 
            actor_response = 'Direita'
        else:
            actor_response = ' '

        # Frame writing
        frame = Utils.write_on_frame(frame, str(np.round(centroid_difference, 2)))
        frame = Utils.write_on_frame(frame, actor_response, position=(50, 250))
        median_displaced_area = displaced_area_series.get_median()
        percentage_displaced_area = np.round(((original_polygon_area - median_displaced_area)/original_polygon_area) * 100, 2)
        frame = Utils.write_on_frame(frame, f"{percentage_displaced_area}%", position=(50, 150))
        cv.drawContours(frame, [original_polygon], -1, Default.green, 2)

        cv.imshow('frame', frame)

        if cv.waitKey(1) == ord('q'):
            main_loop = False

    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()