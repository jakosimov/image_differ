import cv2
import numpy as np
import threading
from copy import deepcopy
from cv2 import VideoWriter, VideoWriter_fourcc, VideoCapture
from collections import deque

FPS = 10 
max_count = 4000
skip_count = 0
frames_to_save = 30 
saved_frames_frequency = 2
emphasis_factor = 10.0
threshold = 10

vidcap = VideoCapture('video.mp4')
success, image = vidcap.read()
width = int(vidcap.get(4))
height = int(vidcap.get(3))
fourcc = VideoWriter_fourcc(*'XVID')
videoWriter = VideoWriter('output.avi', fourcc, float(FPS), (height, width))
count = 0
last_frames = deque()
running_total = np.full((width, height, 3), 0)

print('width =', width)
print('height =', height)

def calculate_frame(image, count):
    global last_frames, running_total

    original_image = np.int32(image)

    should_save_frame = count % saved_frames_frequency == 0

    if len(last_frames) >= frames_to_save:
        average_frame = running_total / frames_to_save
        image = np.absolute(np.subtract(original_image, average_frame))

        # image = np.mean(image, 2)
        image = (image[:,:,0] + image[:,:,1] + image[:,:,2]) / 3
        image = np.repeat(image, 3)
        image = np.resize(image, (width, height, 3))

        image = (image > threshold) * image * emphasis_factor
        if should_save_frame:
            first_frame = last_frames.popleft()
            running_total = np.subtract(running_total, first_frame)
    else:
        image = original_image
        should_save_frame = True

    if should_save_frame:
        last_frames.append(original_image)
        running_total = np.add(running_total, original_image)

    image = np.uint8(image)
    videoWriter.write(image)

while success and count < max_count:
    if count >= skip_count:
        calculate_frame(image, count)
    success, image = vidcap.read()
    print(count)
    count += 1

videoWriter.release()
vidcap.release()
print('Total count:', count)
