import time
import cv2
import copy
import json
import params

# Global variables preset
showHelp = 1
pwidth=params.PHOTO_WIDTH
pheight=params.PHOTO_HEIGHT
loadImagePath = ""
# loadImagePath = "./src/scene_1280x720_1.png"
# Default settings for selecting unfocused 'joint' zone
recX = int(0.475*pwidth)
recY = pheight
recW = int(pwidth/20)


if (showHelp == 1):
    print ('\n    <><><><><><>KEY USAGE<><><><><><>')
    print ('Esc key ---------- exit')
    print ('Enter ------------ save settings to file')
    print ('Left, Right keys - move choosen zone')
    print ('Up, Down keys ---- change width of choosen zone \n')


# If path is empty than capture from camera, else load this file
if (loadImagePath == ''):
    # Import is here for compatibility with desktop usage instead of Raspberry
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    # Initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution=(pwidth,pheight)
    rawCapture = PiRGBArray(camera)

    # Allow the camera to warmup
    time.sleep(0.1)

    # Grab an image from the camera
    camera.hflip = True
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
else:
    image = cv2.imread(loadImagePath)
    if (image is None):
        print ('Can not read image from file \"'+loadImagePath+'\"')
        exit(0)


# Let user choose unfocused zone manually 
while (1):
    imTune = copy.copy(image)
    cv2.rectangle(imTune, (recX,recY), (recX+recW, 0), (0,255,0), 3)
    cv2.imshow("Image", imTune)
    k = cv2.waitKey(0)
    print (k)
    if (k==27) | (k==1048603) | (k==-1): #ESC key, or window closed - just exit
        break
    elif k==-1:
        print k
        continue
    elif (k==65361) | (k==63234) | (k==1113937): #LEFT pressed
        recX = recX-1
    elif (k==65363) | (k==63235) | (k==1113939): #RIGHT pressed
        recX = recX+1
    elif (k==65362) | (k==63232) | (k==1113938): #UP pressed
        recW = recW+1
    elif (k==65364) | (k==63233) | (k==1113940): #DOWN pressed
        recW = recW-1
    elif (k==65421) | (k==13) | (k==10): #ENTER pressed - save results
        minW=min(recX, pwidth-recX-recW)
        leftX1=recX-minW
        leftX2=recX
        rightX1=recX+recW
        rightX2=rightX1+minW 
        print ('imageWidth = ', minW, ' jointWidth=', recW, ' leftIndent=', leftX1, \
                ' rightIndent=', rightX1)
        result = json.dumps({'imageWidth':minW, 'leftIndent':leftX1, \
                            'rightIndent':rightX1, 'jointWidth':recW},sort_keys=True, \
                             indent=4, separators=(',',':'))
        fName = 'pf_'+ str(pwidth) +'_'+str(pheight)+'.txt'
        f = open (str(fName), 'w') 
        f.write(result)
        f.close()
        print ('Settings saved to file'+str(fName))
        break