import logging

import cv2
from matplotlib import pyplot as plt
import numpy as np
import json
from stereovision.calibration import StereoCalibration
import params
from image_handler import ImageHandler

logging.basicConfig(level='INFO')
__metaclass__ = type

class DepthMap(ImageHandler):
    def __init__(self):
        super(DepthMap, self).__init__()

    def split_image(self, imageToDisp):
        return super(DepthMap, self).split_image(imageToDisp)

    def __plot(self, title, img, i):
        plt.subplot(2, 2, i)
        plt.title(title)
        plt.imshow(img, 'gray')
        plt.gca().get_xaxis().set_visible(False)
        plt.gca().get_yaxis().set_visible(False)

    # Depth map function
    def stereo_depth_map(self,rectified_pair, ndisp, sws):
        stereo = cv2.StereoBM_create(numDisparities=ndisp,blockSize= sws)

        # stereo = cv2.StereoBM(cv2.STEREO_BM_BASIC_PRESET, \
        #                       ndisparities=ndisp, SADWindowSize=sws)
        return stereo.compute(rectified_pair[0], rectified_pair[1])

    def build_depth_map(self, image_path):
        logging.info('Load calibration data...')
        calibration = StereoCalibration(input_folder='../ress')
        rectified_pair = calibration.rectify((self.split_image(image_path)))
        disparity = self.stereo_depth_map(rectified_pair, 256, 15)
        logging.info('Building depth map...')
        return rectified_pair, disparity

    def detect_contour(self, disparity):
        ret, thresh = cv.threshold(disparity, 127, 255, 0)
        disparity, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # ret, th = cv2.threshold(gray, 127, 255, 1)
        # kernel = np.ones((15, 15), np.uint8)
        # dilate = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel, 3)
        # contours, hierarchy = cv2.findContours(dilate, 2, 1)
        # cv2.drawContours(self.plot(u'Depth map', disparity/255., 3), contours, -1, (0, 255, 0), 3)
        pass

    def draw_plot(self, rectified_pair, disparity):
        self.__plot(u'Left calibrated', rectified_pair[0], 1)
        self.__plot(u'Right calibrated', rectified_pair[1], 2)
        self.__plot(u'Depth map', disparity/255., 3)
        plt.show()

depthMap = DepthMap()
image = '../scenes/photo.png'
try:
    rectified_pair, disparity = depthMap.build_depth_map(image)
    depthMap.draw_plot(rectified_pair, disparity)
except:
    logging.error("Wrong calibration directory")
    # depthMap.highlight_borders()