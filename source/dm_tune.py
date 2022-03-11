import logging
import os

import cv2
#from picamera.array import PiRGBArray
#from picamera import PiCamera
import matplotlib as mpl
mpl.use('Qt5Agg')
from matplotlib import pyplot as plt

from depth_map import DepthMap
from matplotlib.widgets import Slider, Button

import numpy as np
import json
import image_handler

from stereovision.calibration import StereoCalibration
logging.basicConfig(level='INFO')

# Depth map function
SWS = 5
PFS = 5
PFC = 29
MDS = -25
NOD = 128
TTH = 100
UR = 10
SR = 15
SPWS = 100

def read_parameters(rectified_pair):
    print ('SWS='+str(SWS)+' PFS='+str(PFS)+' PFC='+str(PFC)+' MDS='+\
           str(MDS)+' NOD='+str(NOD)+' TTH='+str(TTH))
    print (' UR='+str(UR)+' SR='+str(SR)+' SPWS='+str(SPWS))
    c, r = rectified_pair[0].shape
    disparity = np.array(c,r)
    sbm = cv2.CreateStereoBMState()
    sbm.SADWindowSize = SWS
    sbm.preFilterType = 1
    sbm.preFilterSize = PFS
    sbm.preFilterCap = PFC
    sbm.minDisparity = MDS
    sbm.numberOfDisparities = NOD
    sbm.textureThreshold = TTH
    sbm.uniquenessRatio= UR
    sbm.speckleRange = SR
    sbm.speckleWindowSize = SPWS
    cv2.FindStereoCorrespondenceBM(rectified_pair[0], rectified_pair[1], disparity, sbm)
    disparity_visual = disparity = np.array(c,r)
    cv2.Normalize(disparity, disparity_visual, 0, 255, cv2.CV_MINMAX)
    disparity_visual = np.array(disparity_visual)
    return disparity_visual


def save_map_settings(event):
    buttons.label.set_text("Saving...")
    logging.info('Saving to file...')
    result = json.dumps({'SADWindowSize': SWS, 'preFilterSize': PFS, 'preFilterCap': PFC, \
                         'minDisparity': MDS, 'numberOfDisparities': NOD, 'textureThreshold': TTH, \
                         'uniquenessRatio': UR, 'speckleRange': SR, 'speckleWindowSize': SPWS}, \
                        sort_keys=True, indent=4, separators=(',', ':'))
    fName = os.getcwd() + '/3dmap_set.txt'
    f = open(str(fName), 'w')
    f.write(result)
    f.close()
    buttons.label.set_text("Save to file")
    print ('Settings saved to file ' + fName)

def load_map_settings( event ):
    global SWS, PFS, PFC, MDS, NOD, TTH, UR, SR, SPWS, loading_settings
    loading_settings = 1
    fName = os.getcwd() + '/3dmap_set.txt'
    print('Loading parameters from file...')
    buttonl.label.set_text ("Loading...")
    try:
        f=open(fName, 'r')
        data = json.load(f)
        sSWS.set_val(data['SADWindowSize'])
        sPFS.set_val(data['preFilterSize'])
        sPFC.set_val(data['preFilterCap'])
        sMDS.set_val(data['minDisparity'])
        sNOD.set_val(data['numberOfDisparities'])
        sTTH.set_val(data['textureThreshold'])
        sUR.set_val(data['uniquenessRatio'])
        sSR.set_val(data['speckleRange'])
        sSPWS.set_val(data['speckleWindowSize'])
        f.close()
    except:
        buttonl.label.set_text("No calib data")

    buttonl.label.set_text ("Load settings")
    logging.info('Parameters loaded from file '+fName)
    logging.info('Redrawing depth map with loaded parameters...')
    loading_settings = 0
    update(0)

def update(val):
    global SWS, PFS, PFC, MDS, NOD, TTH, UR, SR, SPWS
    SWS = int(sSWS.val/2)*2+1 #convert to ODD
    PFS = int(sPFS.val/2)*2+1
    PFC = int(sPFC.val/2)*2+1
    MDS = int(sMDS.val)
    NOD = int(sNOD.val/16)*16
    TTH = int(sTTH.val)
    UR = int(sUR.val)
    SR = int(sSR.val)
    SPWS= int(sSPWS.val)
    if ( loading_settings==0 ):
        logging.info('Rebuilding depth map')
        depthMap = DepthMap()
        image = '../scenes/photo.png'
        rectified_pair, disparity = depthMap.build_depth_map(image)
        # disparity = read_parameters(rectified_pair)
        dmObject.set_data(disparity)
        logging.info('Redraw depth map')
        plt.ion()
        plt.draw()

depthMap = DepthMap()
image = '../scenes/photo.png'
rectified_pair, disparity = depthMap.build_depth_map(image)
# disparity = read_parameters(rectified_pair)

plt.ion()

# Set up and draw interface
# Draw left image and depth map
axcolor = 'yellow'
fig = plt.subplots(1,2)
plt.subplots_adjust(left=0.15, bottom=0.5)
plt.subplot(1,2,1)
dmObject = plt.imshow(rectified_pair[0], 'gray')

saveax = plt.axes([0.3, 0.38, 0.15, 0.04]) #stepX stepY width height
buttons = Button(saveax, 'Save settings', color=axcolor, hovercolor='0.975')

buttons.on_clicked(save_map_settings)

loadax = plt.axes([0.5, 0.38, 0.15, 0.04]) #stepX stepY width height
buttonl = Button(loadax, 'Load settings', color=axcolor, hovercolor='0.975')

buttonl.on_clicked(load_map_settings)

plt.subplot(1,2,2)
dmObject = plt.imshow(disparity, aspect='equal')

# Draw interface for adjusting parameters
logging.info('Start interface creation')

SWSaxe = plt.axes([0.15, 0.01, 0.7, 0.025], facecolor=axcolor) #stepX stepY width height
PFSaxe = plt.axes([0.15, 0.05, 0.7, 0.025], facecolor=axcolor) #stepX stepY width height
PFCaxe = plt.axes([0.15, 0.09, 0.7, 0.025], facecolor=axcolor) #stepX stepY width height
MDSaxe = plt.axes([0.15, 0.13, 0.7, 0.025], facecolor=axcolor) #stepX stepY width height
NODaxe = plt.axes([0.15, 0.17, 0.7, 0.025], facecolor=axcolor) #stepX stepY width height
TTHaxe = plt.axes([0.15, 0.21, 0.7, 0.025], facecolor=axcolor) #stepX stepY width height
URaxe = plt.axes([0.15, 0.25, 0.7, 0.025], facecolor=axcolor) #stepX stepY width height
SRaxe = plt.axes([0.15, 0.29, 0.7, 0.025], facecolor=axcolor) #stepX stepY width height
SPWSaxe = plt.axes([0.15, 0.33, 0.7, 0.025], facecolor=axcolor) #stepX stepY width height

sSWS = Slider(SWSaxe, 'SWS', 5.0, 255.0, valinit=5)
sPFS = Slider(PFSaxe, 'PFS', 5.0, 255.0, valinit=5)
sPFC = Slider(PFCaxe, 'PreFiltCap', 5.0, 63.0, valinit=29)
sMDS = Slider(MDSaxe, 'MinDISP', -100.0, 100.0, valinit=-25)
sNOD = Slider(NODaxe, 'NumOfDisp', 16.0, 256.0, valinit=128)
sTTH = Slider(TTHaxe, 'TxtrThrshld', 0.0, 1000.0, valinit=100)
sUR = Slider(URaxe, 'UnicRatio', 1.0, 20.0, valinit=10)
sSR = Slider(SRaxe, 'SpcklRng', 0.0, 40.0, valinit=15)
sSPWS = Slider(SPWSaxe, 'SpklWinSze', 0.0, 300.0, valinit=100)


# Update depth map parameters and redraw


# Connect update actions to control elements
sSWS.on_changed(update)
sPFS.on_changed(update)
sPFC.on_changed(update)
sMDS.on_changed(update)
sNOD.on_changed(update)
sTTH.on_changed(update)
sUR.on_changed(update)
sSR.on_changed(update)
sSPWS.on_changed(update)

print('Show interface to user')
plt.show(block=True)
