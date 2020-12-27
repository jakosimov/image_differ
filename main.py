import cv2
import numpy as np
import threading
from copy import deepcopy
from cv2 import VideoWriter, VideoWriter_fourcc, VideoCapture
from collections import deque

FPS = 5 

vidcap = VideoCapture('video.mp4')
success, image = vidcap.read()
width = int(vidcap.get(4))
height = int(vidcap.get(3))
fourcc = VideoWriter_fourcc(*'XVID')
videoWriter = VideoWriter('output.avi', fourcc, float(FPS), (height, width))
count = 0
max_count = 100
last_frames = deque()
frames_to_save = 30 
running_total = np.full(width * height * 3, 0)

print('width =', width)
print('height =', height)

def calculate_frame(image):
    global last_frames, running_total
    image = np.matrix.flatten(image)
    image = np.int32(image)
    image_copy = deepcopy(image)
    if len(last_frames) >= frames_to_save:
        average_frame = running_total / frames_to_save
        image = np.absolute(np.subtract(image, average_frame))
        first_frame = last_frames.popleft()
        running_total = np.subtract(running_total, first_frame)
    last_frames.append(image_copy)
    running_total = np.add(running_total, image_copy)
    image = np.uint8(image)
    image = np.resize(image, (width, height, 3)) 
    # print(image)
    videoWriter.write(image)

while success and count < max_count:
    calculate_frame(image)
    success, image = vidcap.read()
    print(count)
    count += 1
videoWriter.release()
vidcap.release()
print('Total count:', count)
