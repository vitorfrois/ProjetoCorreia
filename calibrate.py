import cv2 as cv
import numpy as np
from config import Config, Default
from utils import Utils, FixedSizeList

def multiplier_trackbar_callback(value):
    global multiplier
    multiplier = np.round(value * 1e-3, 3)
    print(multiplier)

def threshold_trackbar_callback(value):
    global threshold
    threshold = value
    print(threshold)

class Calibrate:
    def get_threshold(cap: cv.VideoCapture) -> int:
        calibrating = True

        cv.namedWindow('frame')
        cv.createTrackbar('Threshold', 'frame', 127, 255, threshold_trackbar_callback)
        
        while calibrating:
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            imgray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            _, thresh = cv.threshold(imgray, threshold, 100, cv.THRESH_BINARY)

            pressed_key = cv.waitKey(1)
            if pressed_key == ord(' '):
                calibrating = False

            thresh = Utils.write_on_frame(thresh, str(threshold))
            cv.imshow('frame', thresh)
        
        cv.destroyWindow('frame')
        return threshold

    def get_multiplier(cap: cv.VideoCapture, threshold: int) -> np.array:
        calibrating = True

        width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

        image_series = FixedSizeList(10)

        cv.namedWindow('frame')

        cv.createTrackbar('Multiplier', 'frame', 1, 100, multiplier_trackbar_callback)

        while calibrating:
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            
            processed_image = Utils.process_image(frame, threshold)
            image_series.append(processed_image)
            image_median = image_series.get_median({'axis': 0}).astype("uint8")
            image_median = cv.medianBlur(image_median, 3)

            try:
                polygon_contour = Utils.get_object_polygon_contour(image_median, multiplier)
                cv.drawContours(frame, [polygon_contour], -1, (0,255,0), 2)
            except Exception as e:
                print('nenhum contorno', e)

            pressed_key = cv.waitKey(1)
            if pressed_key == ord(' '):
                calibrating = False

            frame = Utils.write_on_frame(frame, str(multiplier))

            cv.imshow('frame', frame)

        cv.destroyWindow('frame')
        return polygon_contour, multiplier