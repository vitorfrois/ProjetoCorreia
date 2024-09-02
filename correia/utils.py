import cv2 as cv
import numpy as np
from .config import Default

class Utils:
    def get_object_polygon_contour(image: np.array, multiplier: float = 0.01) -> list:
        try:
            contours,hierarchy = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            area_list = np.array([cv.contourArea(contour) for contour in contours])
            object_countour_index = np.argmax(area_list)
            contour = contours[object_countour_index]
            epsilon = multiplier * cv.arcLength(contour,True)
            approx = cv.approxPolyDP(contour,epsilon,True)
        except Exception as e:
            print('nenhum contorno', e)
            return []
        return approx

    def process_image(image, threshold: int = 127) -> np.array:
        imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        _, thresh = cv.threshold(imgray, threshold, 255, cv.THRESH_BINARY_INV)
        processed_image = cv.morphologyEx(thresh, cv.MORPH_OPEN, Default.kernel)
        processed_image = cv.morphologyEx(processed_image, cv.MORPH_DILATE, Default.kernel, iterations=3)
        return processed_image

    def write_on_frame(frame: np.array, text: str, position: tuple = Default.org) -> np.array:
        return cv.putText(
            frame, text, position, Default.font, 
            Default.font_scale, Default.blue, 
            Default.thickness, cv.LINE_AA
        )

class FixedSizeList:
    def __init__(self, size: int = 20):
        self.list = []
    def append(self, element):
        if len(self.list) > 20:
            self.list[:-1] = self.list[1:]
            self.list[-1] = element
        else:
            self.list.append(element)
    def get_median(self, kwargs: dict = {}):
        return np.median(self.list, **kwargs)

