import numpy as np
import processer
from collections import deque
import sys

file_name = sys.argv[1]
max_count = -1
if len(sys.argv) >= 3:
   max_count = int(sys.argv[2])

input_file = '' + file_name + '.mp4'
output_file = 'out_' + file_name + '.avi'
emphasis_factor = 50.0
threshold = 2.0
neighbour_threshold = 10
average_threshold = 3.0

frames_to_save = 30
saved_frames_frequency = 3
frames_to_skip = 300

processer = processer.Processer(input_file, output_file, max_count=max_count)
width = processer.width
height = processer.height

last_frames = deque()
running_total = np.full((width, height, 3), 0)

def scale_by_factor(image):
    return image * emphasis_factor

def to_pixel_form(image):
    image = np.uint32(image)
    return (image[:,:,0] + image[:,:,1] + image[:,:,2]) / 3

def from_pixel_form(image):
    image = np.minimum(image, 255)
    image = np.repeat(image, 3)
    image = np.resize(image, (width, height, 3))
    image = np.uint8(image)

    return image

def get_sum_of_neighbours(image):
    bot = np.pad(image[1:,:], ((0, 1), (0, 0)), constant_values=(0))
    top = np.pad(image[:-1,:], ((1, 0), (0, 0)), constant_values=(0))
    right = np.pad(image[:,1:], ((0, 0), (0, 1)), constant_values=(0)) 
    left = np.pad(image[:,:-1], ((0, 0), (1, 0)), constant_values=(0))
    return bot + top + right + left

def filter_by_neighbours(image):
    neighbours = get_sum_of_neighbours(image)
    return (neighbours >= neighbour_threshold) * image 

with open(file_name + '_total.npy', 'rb') as f:
    total = np.load(f, allow_pickle=True)
    total = np.resize(total, (width, height, 3))
    total = to_pixel_form(total)

average_total = np.mean(total)
total = total * (total >= (average_total * average_threshold))

def apply_threshold(image):
    return (image >= threshold) * image

def filter_out_by_total(image):
    image = image * (total == 0)
    return image

last_frame = np.full((width, height), 0)
def filter_by_last_empty(image):
    global last_frame
    temp_frame = image * (last_frame > 0.0)
    last_frame = image
    image = temp_frame
    return image

def filter_by_non_empty_neighbours(image):
    neigh = get_sum_of_neighbours(image)
    image = image * (neigh > 0.1)
    return image

def calculate_frame(image, count, width, height):
    global last_frames, running_total

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

    image = to_pixel_form(image)

    image = filter_out_by_total(image)
    image = apply_threshold(image)

    image = filter_by_neighbours(image)

    image = scale_by_factor(image)
    image = filter_by_last_empty(image)

    image = from_pixel_form(image)

    return image

if __name__ == "__main__":
    processer.run(calculate_frame)
