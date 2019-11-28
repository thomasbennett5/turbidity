#!/usr/bin/python
import time
import picamera
import picamera.array
import numpy as np
import matplotlib.pyplot as plt

'''
cam.start_preview()

time.sleep(1000)

cam.resolution = (2592, 1944)
cam.exposure_mode = 'off'
cam.capture('/home/pi/Desktop/test.jpg')
'''

'''
width = 100
height = 100
stream = open('image.data', 'w+b')
# Capture the image in YUV format
with picamera.PiCamera() as camera:
    camera.resolution = (width, height)
    camera.start_preview()
    time.sleep(2)
    camera.capture(stream, 'yuv')
# Rewind the stream for reading
stream.seek(0)
# Calculate the actual image size in the stream (accounting for rounding
# of the resolution)
fwidth = (width + 31) // 32 * 32
fheight = (height + 15) // 16 * 16
# Load the Y (luminance) data from the stream
Y = np.fromfile(stream, dtype=np.uint8, count=fwidth*fheight).\
        reshape((fheight, fwidth))
'''

with picamera.PiCamera() as camera:
    with picamera.array.PiYUVArray(camera) as stream:
        camera.resolution = (1000, 800)
        #camera.start_preview()
        #time.sleep(2)
        camera.capture(stream, 'yuv')
        # Show size of YUV data
        print(stream.array.shape)
        # Show size of RGB converted data
        print(stream.rgb_array.shape)

img_arr = stream.rgb_array



aoi = img_arr[350:480,180:650,0]

whiteArea = np.average(aoi[:,:100])
blackArea = np.average(aoi[:,200:300])

plt.figure(1)
plt.imshow(img_arr[350:480,180:650,0])

plt.figure(2)
plt.text(50,  1  , "White mean : " + str(whiteArea))
plt.text(200, 0.5, "Black mean : " + str(blackArea))
plt.text(350, 0  , "Difference : " + str(whiteArea - blackArea))



plt.show()