import sys
import numpy as np
import pygame
import pygame.camera
import datetime as dt


def generate_mask(res):
    mask = np.zeros(res)
    
def contrast_measurement(image, box1, box2):
    data = pygame.surfarray.array2d(image).T*255.0/16581375
    print np.min(data)
        
    avg1 = np.average(data[box1[1]:box1[1]+box1[3], box1[0]:box1[0]+box1[2]])
    avg2 = np.average(data[box2[1]:box2[1]+box2[3], box2[0]:box2[0]+box2[2]])
    print avg1, avg2, avg1-avg2
    contrast = abs(avg1-avg2)

    
    return contrast

def display_values(text, location, size = 20):
    font = pygame.font.Font('freesansbold.ttf', size)
    txtSurf = font.render(text, True, WHITE)
    txtRect = txtSurf.get_rect()
    txtRect.topleft = location
    screen.blit(txtSurf, txtRect)
    #pygame.display.update()
    return txtSurf
    
    
#make some colours
BLUE = (0  ,0 ,255)
RED  = (255,0 ,0)
BLACK= (0  ,0 ,0)
WHITE= (255,255,255)
GREEN= (0,255,0)

## set up some window and image resolutions
window      = (640,480)
resolution  = (320,240)
box1        = (170,120,100,200)
box2        = (370,120,100,200)

readyBox    = (645, 450, 100,20)

#set up pygame window and camera
pygame.init()
pygame.camera.init()

screen = pygame.display.set_mode((840,480), 0)
pygame.display.set_caption("Video Turbidity Analysis")
 

cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0],(640,480))
cam.start()

contrast_average = np.zeros(20)

while True:
    screen.fill(BLACK)
    image1 = cam.get_image()
    image1 = pygame.transform.scale(image1, (640,480))
    screen.blit(image1, (0,0))
    contrast = contrast_measurement(image1,box1, box2)
    contrast_average = np.roll(contrast_average,1)
    contrast_average[0] = contrast

    display_values("Contrast Value:", (645, 5))
    display_values(str(np.average(contrast_average)), (645, 25))
    display_values("Press 'P' to save screenshot", (645, 50), size = 14)
    
    if np.std(contrast_average) < 0.8:
        pygame.draw.rect(screen,GREEN, readyBox,0)
        display_values("Ready", readyBox[0:2])
        

    else:
        pygame.draw.rect(screen, RED, readyBox, 0)
        display_values("Unstable", readyBox[0:2])
        display_values("Wait!", (250,50), size = 60)      
        
    
    
    pygame.draw.rect(screen,BLUE, box1, 1) 
    pygame.draw.rect(screen,RED , box2, 1)  
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                fname = dt.datetime.now().strftime('%H:%M:%S')
                pygame.image.save(screen, "screenshot - "+ fname +".jpeg")
        if event.type == pygame.QUIT:
            cam.stop()
            pygame.quit()
            sys.exit()
