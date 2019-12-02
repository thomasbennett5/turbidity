import picamera
from PIL import Image
from time import sleep
import numpy as np
camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 24
camera.start_preview()

# Load the arbitrarily sized image
box = np.zeros((720,1280, 3), dtype=np.uint8)
box[40:60, 40:60] = 0x80

im1 = Image.fromarray(box)
im1.save('test.png')
img = Image.open('test.png')

# Add the overlay with the padded image as the source,
# but the original image's dimensions`
o = camera.add_overlay(np.getbuffer(box))
# By default, the overlay is in layer 0, beneath the
# preview (which defaults to layer 2). Here we make
# the new overlay semi-transparent, then move it above
# the preview
o.alpha = 128
o.layer = 3



# Wait indefinitely until the user terminates the script
while True:
    camera.annotate_text = "Some text"
    sleep(1)
