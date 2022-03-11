import logging
import os
import cv2
import numpy as np
import json
from stereovision.calibration import StereoCalibrator
from stereovision.calibration import StereoCalibration
from params import *
from image_handler import ImageHandler

#logging.basicConfig(level='INFO')
__metaclass__ = type

class Calibrator(ImageHandler):
    # Global variables preset
    def __init__(self):
        super(Calibrator, self).__init__()

    def take_photos(self):
        self.calibrator = StereoCalibrator(self.rows, self.columns, self.square_size, self.image_size)
        photo_counter = FIRST_PHOTO
        print ('Start cycle')

        while photo_counter != TOTAL_PHOTOS:
          photo_counter = photo_counter + 1
          print ('Import pair No ' + str(photo_counter))
          leftName = '../pairs/left_'+str(photo_counter).zfill(2)+'.png'
          rightName = '../pairs/right_'+str(photo_counter).zfill(2)+'.png'
          if os.path.isfile(leftName) and os.path.isfile(rightName):
              imgLeft = cv2.imread(leftName,1)
              imgRight = cv2.imread(rightName,1)
              self.calibrator.add_corners((imgLeft, imgRight), True)
              pass
        print ('End cycle')

    def calibrate_camera(self):
        logging.info('Starting calibration... It can take several minutes!')
        calibration = self.calibrator.calibrate_cameras()
        calibration.export('ress')
        logging.info('Calibration complete!')
        # Lets rectify and show last pair after  calibration


    def show_rectified_pair(self, number_of_image):
        calibration = StereoCalibration(input_folder='../ress')
        leftName = '../pairs/left_' + str(number_of_image).zfill(2) + '.png'
        rightName = '../pairs/right_' + str(number_of_image).zfill(2) + '.png'
        imgLeft = cv2.imread(leftName, 1)
        imgRight = cv2.imread(rightName, 1)
        self.rectified_pair = calibration.rectify((imgLeft, imgRight))
        cv2.imshow('Left CALIBRATED', self.rectified_pair[0])
        cv2.imshow('Right CALIBRATED', self.rectified_pair[1])
        cv2.imwrite("rectifyed_left.jpg",self.rectified_pair[0])
        cv2.imwrite("rectifyed_right.jpg",self.rectified_pair[1])
        cv2.waitKey(0)


