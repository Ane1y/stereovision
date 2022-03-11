
import json
import logging
import os
import time
#import picamera
import cv2

import params
from image_handler import ImageHandler


class PhotoSequence():
    def __init__(self, total_photos=15):
        self.photo_width = 1280
        self.photo_height = 720
        if total_photos >= 1:
            self.total_photos = total_photos
        else:
            raise IOError("The quantity of total photos can not be less than one")

    def take_photos(self, countdown=5):
        if countdown < 1 or not(isinstance(countdown, int)):
            raise IOError("Countdows must be more than 1 and be integer")
        photo_counter = 0    # Photo counter
        #wn = cv2.namedWindow('preview', cv2.WINDOW_NORMAL)

        print "Starting photo sequence"
        if True:
        #with picamera.PiCamera() as camera:
            #camera.resolution = (self.photo_width, self.photo_height)
            #camera.start_preview()
            #camera.preview.fullscreen = False
            #camera.preview.window = (0,0,self.photo_width/2,self.photo_height/2)
            #camera.annotate_text_size = 160
            #camera.annotate_background = picamera.Color('red')
            #camera.hflip = True
            while photo_counter != self.total_photos:
              photo_counter = photo_counter + 1
              filename = 'scene_'+str(self.photo_width)+'x'+str(self.photo_height)+'_'+\
                          str(photo_counter) + '.png'
              cntr = countdown
              while cntr >0:
                #camera.annotate_text = str(cntr)
                cntr-=1
                time.sleep(1)
              #camera.annotate_text = ''
              #camera.capture (filename, use_video_port=True)
              logging.info(' ['+str(photo_counter)+' of '+str(self.total_photos)+'] '+filename)

        logging.info("Finished photo sequence")

    def pair_images(self):
        params_file = '../src/pf_' + str(self.photo_width) + '_' + str(self.photo_height) + '.txt'
        photo_counter = 0
        hand = ImageHandler()
        # Main pair cut cycle
        if (os.path.isdir("../pairs") == False):
            os.makedirs("./pairs")
        while photo_counter != self.total_photos:
            photo_counter += 1
            filename = '../src/scene_' + str(self.photo_width) + 'x' + str(self.photo_height) + \
                       '_' + str(photo_counter) + '.png'
            imgLeft, imgRight = hand.split_image(filename)
            leftName = '../pairs/left_' + str(photo_counter).zfill(2) + '.png'
            rightName = '../pairs/right_' + str(photo_counter).zfill(2) + '.png'
            write_stat = cv2.imwrite(leftName, imgLeft)
            write_stat2 = cv2.imwrite(rightName, imgRight)
            if write_stat or write_stat2 is False:
                raise IOError("can not write pairs")
            logging.info('Pair No ' + str(photo_counter) + ' saved.')

        logging.info('End cycle')