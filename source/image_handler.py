import json
import logging

import cv2

from params import *
__metaclass__ = type

class ImageHandler():
    def __init__(self):
        self.photo_width = PHOTO_WIDTH
        self.photo_height = PHOTO_HEIGHT
        self.params_file = '../src/pf_' + str(self.photo_width) + '_' + str(self.photo_height) + '.txt'
        # Chessboard parameters
        self.rows = 6
        self.columns = 9
        self.square_size = 2.5

        # Read pair cut parameters
        f = open(self.params_file, 'r')
        data = json.load(f)
        self.imageWidth = data['imageWidth']
        self.jointWidth = data['jointWidth']
        self.leftIndent = data['leftIndent']
        self.rightIndent = data['rightIndent']
        f.close()
        self.image_size = (self.imageWidth - WIDTH_OFFSET, self.photo_height)

    def split_image(self, imageToDisp):
        logging.info('Reading image rof depth map...')
        pair_img = cv2.imread(imageToDisp,0)
        if pair_img is None:
            raise OSError("File not found")
        imgLeft = pair_img [0:self.photo_height,self.leftIndent:self.imageWidth]
        cv2.imwrite("../left_sample.jpg", imgLeft)#Y+H and X+W
        imgRight = pair_img [0:self.photo_height,self.rightIndent:self.rightIndent+self.imageWidth-50]
        cv2.imwrite("../right_sample.jpg", imgRight)
        return imgLeft, imgRight
