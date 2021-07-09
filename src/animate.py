#########################################
#
#   Mimics sand animation by creating
#       a video out of an image
#
#                   by
#
#            Code Monkey King
#
#########################################

# packages
import cv2
import numpy as np
from cv2 import VideoWriter
from cv2 import VideoWriter_fourcc
import random
import json

# read & parse settings
with open('settings.json') as f:
    settings = json.loads(f.read())

# load images
source_image = cv2.imread(settings['source_image'])
background_image = cv2.imread(settings['background_image'])
foreground_image = cv2.imread(settings['foreground_image'])

# create video stream
video = VideoWriter(
    settings['output_video'],
    VideoWriter_fourcc(*'MP42'),
    float(25),
    (background_image.shape[1], background_image.shape[0])
)

# convert image to grayscale        
image_grayscale = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
    
# use Canny edge detection for black and white images
if settings['Black-n-White']:
    # detect image edges
    edges = cv2.Canny(image_grayscale, 0, 255)

# use better edge detection for RGB and grayscale images
else:
    # reduce image noice
    image_blur = cv2.medianBlur(image_grayscale, 7)

    # extract edges
    edges = cv2.adaptiveThreshold(
        image_blur,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        blockSize=7,
        C=2
    )

# get image contours 
contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# preview image
if settings['preview']:
    # init preview image
    mask = np.zeros(source_image.shape, np.uint8)
    mask.fill(255)
    cv2.drawContours(mask, contours, -1, (0, 0, 0), settings['line_thickness'] * 2 + 1)
    preview_image = cv2.bitwise_and(mask, background_image)
    if settings['background_image'] != './Images/background_white.png':
        cv2.drawContours(preview_image, contours, -1, (255, 255, 255), settings['line_thickness'])
        preview_image = cv2.bitwise_and(preview_image, foreground_image)
        
    # show preview window
    cv2.imshow('Press any key to continue...', preview_image)

    # clean ups
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# frames counter
frames = 0

# random contour traversal order
random_contour = list(range(len(contours)))
random.shuffle(random_contour)

# loop ove contours
for contour in range(len(contours)):
    # get next contour
    if settings['random_traversal']: next_contour = random_contour[contour]
    else: next_contour = len(contours) - 1 - contour
    
    # draw contour
    for line in range(len(contours[next_contour])):
        # coords to draw at
        x = contours[next_contour][line][0][0]
        y = contours[next_contour][line][0][1]
        
        # draw pixel on frame
        cv2.circle(
            background_image,                     # frame to write pixel to
            (x, y),                               # center coordinates of a circle
            settings['line_thickness'],                                    # circle radius
            (int(foreground_image[y][x][0]),      # pixel RED value
             int(foreground_image[y][x][1]),      # pixel GREEN value
             int(foreground_image[y][x][2])),     # pixel BLUE value 
            settings['line_thickness']           # thickness
        )
        
        # set animation speed
        if settings['animation_speed']:
            if line % settings['animation_speed'] == 0:
                frames += 1
                print('Writing frame:', frames)
                video.write(background_image)

    # write video frame
    frames += 1
    print('Writing frame:', frames)
    video.write(background_image)

# show complete image
for frame in range(settings['complete_image_show_frames']):
    # write video frame
    frames += 1
    print('Writing frame:', frames)
    video.write(background_image)
    
# release video stream
video.release()


