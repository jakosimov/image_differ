import cv2
import numpy as np
import threading
from copy import deepcopy
from cv2 import VideoWriter, VideoWriter_fourcc, VideoCapture

def pixel_difference(pix1, pix2):
    if pix1[0] > pix2[0]:
        pix1[0] = pix1[0] - pix2[0]
    else:
        pix1[0] = pix2[0] - pix1[0]

    if pix1[1] > pix2[1]:
        pix1[1] = pix1[1] - pix2[1]
    else:
        pix1[1] = pix2[1] - pix1[1]

    if pix1[2] > pix2[2]:
        pix1[2] = pix1[2] - pix2[2]
    else:
        pix1[2] = pix2[2] - pix1[2]

FPS = 1

vidcap = VideoCapture('video.mp4')
success, image = vidcap.read()
width = int(vidcap.get(4))
height = int(vidcap.get(3))
fourcc = VideoWriter_fourcc(*'XVID')
videoWriter = VideoWriter('output.avi', fourcc, float(FPS), (height, width))
count = 0
max_count = 10
last_frames = []

number_of_threads = 1
thread_span = int(width / number_of_threads)
print('width =', width)
print('height =', height)

def for_thread(image, last_frame, index, check_list):
    def result():
        start_x = thread_span * index
        for x in range(start_x, start_x + thread_span):
            for y in range(height):
                pixel_difference(image[x][y], last_frame[x][y])
        check_list[index] = True

    return result
    

def calculate_frame(image):
    global last_frames
    image_copy = deepcopy(image)
    if len( last_frames ) >= 1:
        last_frame = last_frames[-1]
        check_list = [False] * number_of_threads
        for index in range(number_of_threads):
            thread = threading.Thread(target=for_thread(image, last_frame, index, check_list))
            thread.setDaemon(True)
            thread.start()
        while not all(check_list): 
            pass
        last_frames = last_frames[1:]
    last_frames.append(image_copy)
    videoWriter.write(image)

while success and count < max_count:
    calculate_frame(image)
    success, image = vidcap.read()
    print(count)
    count += 1
videoWriter.release()
vidcap.release()
print('Total count:', count)
