import cv2 as cv
import numpy as np
from dataclasses import dataclass
import configparser

class Default:
    font = cv.FONT_HERSHEY_SIMPLEX
    org = (50, 50)
    font_scale = 1
    white = (255, 255, 255)
    blue = (255, 0, 0)
    red = (0, 255, 0)
    green = (0, 0, 255)
    thickness = 2
    kernel = np.ones((3,3),np.uint8)

@dataclass
class Config:
    config_file = 'config.ini'
    tolerance: int
    image_interval: float
    threshold: int
    multiplier: float

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.read()

    def read(self):
        self.config.read(self.config_file)
        self.tolerance = int(self.config['DEFAULT']['tolerance'])
        self.image_interval = float(self.config['DEFAULT']['image_interval'])
        self.threshold = int(self.config['DEFAULT']['threshold'])
        self.multiplier = float(self.config['DEFAULT']['multiplier'])

    def save(self):
        self.config['DEFAULT']['tolerance'] = str(self.tolerance)
        self.config['DEFAULT']['image_interval'] = str(self.image_interval)
        self.config['DEFAULT']['threshold'] = str(self.threshold)
        self.config['DEFAULT']['multiplier'] = str(self.multiplier)
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

