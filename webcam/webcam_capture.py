#!/usr/bin/python
from picamera import PiCamera
import time

cam = PiCamera()

cam.start_preview()

time.sleep(1000)

cam.resolution = (2592, 1944)
cam.exposure_mode = 'off'



cam.capture('/home/pi/Desktop/test.jpg')
