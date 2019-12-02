import picamera
import numpy as np
from picamera.array import PiRGBAnalysis
from picamera.color import Color

class contrastAnalyser(PiRGBAnalysis):
    def __init__(self, camera):
        super(contrastAnalyser, self).__init__(camera)
        

    def analyze(self, a):
        x =1


def make_box(box_coords, img_res, array = 0):
    if type(array) == type(0):
        box = np.zeros((img_res[1]+6, img_res[0], 3), dtype=np.uint8)
        box[box_coords[0]:box_coords[1], box_coords[2]:box_coords[3], :] = 0x80
    
    if type(array) != type(0):
        box = array
        box[box_coords[0]:box_coords[1], box_coords[2]:box_coords[3], :] = 0x80
    
    return box


image_resolution = [160,90] ## [width / x, height / y]

with picamera.PiCamera(resolution=str(image_resolution[0])+'x'+str(image_resolution[1]), framerate=24) as camera:
    ## Box Coords = [y0, y1, x0, x1]
    box_coords_1 = [30,60,50,80]
    box_coords_2 = [30,60,90,120]

  
    # Fix the camera's white-balance gains
    #camera.awb_mode = 'off'
    #camera.awb_gains = (1.4, 1.5)
    # Dra#w a box over the area we're going to watch
    camera.start_preview(alpha=255)
    
    #box = np.zeros((90,160, 3), dtype=np.uint8)
    #box[30:60, 60:120, :] = 0x80

    box = make_box(box_coords_1, image_resolution)
    box = make_box(box_coords_2, image_resolution, box)

    camera.add_overlay(np.getbuffer(box), size=(160, 90),alpha = 100, layer=3)

    

    # Construct the analysis output and start recording data to it
    with contrastAnalyser(camera) as analyser:
        camera.start_recording(analyzer, 'rgb')
        try:
            while True:
                camera.wait_recording(1)
        finally:
            camera.stop_recording()
