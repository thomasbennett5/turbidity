import sys
import numpy as np
import pygame
import pygame.camera
import datetime as dt


def generate_mask(res):
    mask = np.zeros(res)
    
def contrast_measurement(image, box1, box2):
    data = pygame.surfarray.array2d(image).T*255.0/16581375
    #print np.min(data)
        
    avg1 = np.average(data[box1[1]:box1[1]+box1[3], box1[0]:box1[0]+box1[2]])
    avg2 = np.average(data[box2[1]:box2[1]+box2[3], box2[0]:box2[0]+box2[2]])
    #print avg1, avg2, avg1-avg2
    contrast = abs(avg1-avg2)

    
    return contrast

def display_values(text, location, size = 15):
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
imgSize     = (int(window[0]*0.9), int(window[1]*0.9))
resolution  = (320,240)
box1        = (180,120,100,200)
box2        = (360,120,100,200)
readyBox    = (10, 450, 100,20)
saveBox     = (200,450, 100,20)

#set up pygame window and camera
pygame.init()
pygame.camera.init()
screen = pygame.display.set_mode((720,480), 0)
pygame.display.set_caption("Video Turbidity Analysis")
 
## Initialise Camera
cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0],(640,480))
cam.start()

## Set up save box
input_box = pygame.Rect(saveBox)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
done = False


contrast_average = np.zeros(20)

while True:
    screen.fill(BLACK)
    image1 = cam.get_image()
    image1 = pygame.transform.scale(image1, imgSize)
    screen.blit(image1, (0,0))
    contrast = contrast_measurement(image1,box1, box2)
    contrast_average = np.roll(contrast_average,1)
    contrast_average[0] = contrast

    display_values("Contrast Value:", (580, 5))
    display_values(str(np.average(contrast_average)), (580, 25))
    display_values("Press 'P' to save screenshot", (580, 25), size = 10)
    display_values("Press 'S' to save with filename", (350, 450), size = 10)
    
    if np.std(contrast_average) < 0.8:
        pygame.draw.rect(screen,GREEN, readyBox,0)
        display_values("Ready", readyBox[0:2])
        

    else:
        pygame.draw.rect(screen, RED, readyBox, 0)
        display_values("Unstable", readyBox[0:2])
        display_values("Wait!", (250,50), size = 60)      
    
    # Render the current text.
    txt_surface = font.render(text, True, color)
    # Resize the box if the text is too long.
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    # Blit the text.
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    # Blit the input_box rect.
    pg.draw.rect(screen, color, input_box, 2)
    
    
    pygame.draw.rect(screen,BLUE, box1, 1) 
    pygame.draw.rect(screen,RED , box2, 1)  
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                    if event.key == pg.K_s:
                        pygame.image.save(screen, text +".jpeg")
                        text = ''
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                    
            if event.key == pygame.K_p:
                fname = dt.datetime.now().strftime('%H:%M:%S')
                pygame.image.save(screen, "screenshot - "+ fname +".jpeg")
        if event.type == pygame.QUIT:
            cam.stop()
            pygame.quit()
            sys.exit()
