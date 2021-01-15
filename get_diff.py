import processer
import numpy as np
from collections import deque
import sys

file_name = sys.argv[1]

input_file = file_name + '.mp4'
output_file = 'diff_' + file_name + '.avi'
frames_to_save = 45 
saved_frames_frequency = 3
frames_to_skip = 300

processer = processer.Processer(input_file, output_file, max_count=-1)
width = processer.width
height = processer.height
last_frames = deque()
running_total = np.full((width, height, 3), 0)

total = np.full((width, height, 3), 0)

print('width =', width)
print('height =', height)

def calculate_frame(image, count, width, height):
    global last_frames, running_total, total

    original_image = np.int32(image)

    should_save_frame = count >= frames_to_skip and count % saved_frames_frequency == 0

    if len(last_frames) >= frames_to_save:
        average_frame = running_total / frames_to_save
        image = np.absolute(np.subtract(original_image, average_frame))

        if should_save_frame:
            first_frame = last_frames.popleft()
            running_total = np.subtract(running_total, first_frame)
    else:
        image = np.full((width, height, 3), 0)
        # should_save_frame = True

    if should_save_frame:
        last_frames.append(original_image)
        running_total = np.add(running_total, original_image)

    total = total + image

    image = np.uint8(image)
    return image

processer.run(calculate_frame)
with open(file_name + '_total.npy', 'wb') as f:
    total = np.resize(total, (width*height*3,))
    np.save(f, total)
    
    
