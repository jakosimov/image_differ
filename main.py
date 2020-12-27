import cv2
import numpy as np
import threading
from copy import deepcopy
from cv2 import VideoWriter, VideoWriter_fourcc, VideoCapture

FPS = 5

vidcap = VideoCapture('video.mp4')
success, image = vidcap.read()
width = int(vidcap.get(4))
height = int(vidcap.get(3))
fourcc = VideoWriter_fourcc(*'XVID')
videoWriter = VideoWriter('output.avi', fourcc, float(FPS), (height, width))
count = 0
max_count = 100
last_frames = []

number_of_threads = 1
thread_span = int(width / number_of_threads)
print('width =', width)
print('height =', height)

def calculate_frame(image):
    global last_frames
    image = np.matrix.flatten(image)
    # image = np.int8(image)
    image_copy = deepcopy(image)
    if len(last_frames) >= 1:
        last_frame = last_frames[-1]
        image = np.subtract(np.maximum(image, last_frame), np.minimum(image, last_frame))
        last_frames = last_frames[1:]
    last_frames.append(image_copy)
    # image = np.uint8(image)
    image = np.resize(image, (width, height, 3)) 
    videoWriter.write(image)

while success and count < max_count:
    calculate_frame(image)
    success, image = vidcap.read()
    print(count)
    count += 1
videoWriter.release()
vidcap.release()
print('Total count:', count)
