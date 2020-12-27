import cv2
import numpy as np
import threading
from copy import deepcopy
from cv2 import VideoWriter, VideoWriter_fourcc, VideoCapture
from collections import deque

FPS = 5 
max_count = 500
frames_to_save = 30 
saved_frames_frequency = 2
emphasis_factor = 1.0

vidcap = VideoCapture('video.mp4')
success, image = vidcap.read()
width = int(vidcap.get(4))
height = int(vidcap.get(3))
fourcc = VideoWriter_fourcc(*'XVID')
videoWriter = VideoWriter('output.avi', fourcc, float(FPS), (height, width))
count = 0
last_frames = deque()
running_total = np.full(width * height * 3, 0)

print('width =', width)
print('height =', height)

def calculate_frame(image, count):
    global last_frames, running_total

    image = np.matrix.flatten(image)
    original_image = np.int32(image)

    should_save_frame = count % saved_frames_frequency == 0

    if len(last_frames) >= frames_to_save:
        average_frame = running_total / frames_to_save
        image = emphasis_factor * np.absolute(np.subtract(original_image, average_frame))

        if should_save-frame:
            first_frame = last_frames.popleft()
            running_total = np.subtract(running_total, first_frame)
    else:
        image = original_image

    if should_save_frame:
        last_frames.append(original_image)
        running_total = np.add(running_total, original_image)

    image = np.uint8(image)
    image = np.resize(image, (width, height, 3)) 
    videoWriter.write(image)

while success and count < max_count:
    calculate_frame(image, count)
    success, image = vidcap.read()
    print(count)
    count += 1

videoWriter.release()
vidcap.release()
print('Total count:', count)
