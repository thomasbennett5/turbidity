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

y0 = 350
y1 = 480
x0 = 180
x1 = 650

whiteArea_start = x0
whiteArea_stop  = x0 + 100
whiteArea_width = whiteArea_stop - whiteArea_start
whiteArea_height= y1 - y0

blackArea_start = x0 + 200
blackArea_stop  = x0 + 300
blackArea_width = blackArea_stop - blackArea_start
blackArea_height= y1 - y0

aoi = img_arr[350:480,180:650,0]

whiteArea_avg = np.average(img_arr[y0:y1, whiteArea_start:whiteArea_stop])
blackArea_avg = np.average(img_arr[y0:y1, blackArea_start:blackArea_stop])

print "White area average : ", whiteArea
print "Black area average : ", blackArea
print "Difference         : ", whiteArea - blackArea

fig = plt.figure()

img = fig.add_subplot(2,1,1)
img.imshow(img_arr)

rect = patches.Rectangle((whiteArea_start,y0),whiteArea_width,whiteArea_height,linewidth=1,edgecolor='r',facecolor='none')
img.add_patch(rect)

text = fig.add_subplot(2,1,2)
text.get_xaxis().set_visible(False)
text.get_yaxis().set_visible(False)
text.text(0.2, 0.6 , "White mean : " + str(whiteArea))
text.text(0.2, 0.5 , "Black mean : " + str(blackArea))
text.text(0.2, 0.4 , "Difference : " + str(whiteArea - blackArea))



plt.show()