
import numpy as np
import processer
import sys

file_name = sys.argv[1]

input_file = 'diff_' + file_name + '.avi'
output_file = 'out_' + file_name + '.avi'
emphasis_factor = 50.0
threshold = 0.5
neighbour_threshold = 10
average_threshold = 3.0

processer = processer.Processer(input_file, output_file, max_count=1000)
width = processer.width
height = processer.height

def scale_by_factor(image):
    return image * emphasis_factor

def to_pixel_form(image):
    image = np.uint32(image)
    return (image[:,:,0] + image[:,:,1] + image[:,:,2]) / 3

with open(file_name + '_total.npy', 'rb') as f:
    total = np.load(f, allow_pickle=True)
    total = np.resize(total, (width, height, 3))
    total = to_pixel_form(total)

def from_pixel_form(image):
    image = np.minimum(image, 255)
    image = np.repeat(image, 3)
    image = np.resize(image, (width, height, 3))
    image = np.uint8(image)

    return image

average_total = np.mean(total)
total = total * (total >= (average_total * average_threshold))
# total = from_pixel_form(total)


total_difference = np.full((width, height), 1) 

print('width =', width)
print('height =', height)

def get_sum_of_neighbours(image):
    bot = np.pad(image[1:,:], ((0, 1), (0, 0)), constant_values=(0))
    top = np.pad(image[:-1,:], ((1, 0), (0, 0)), constant_values=(0))
    right = np.pad(image[:,1:], ((0, 0), (0, 1)), constant_values=(0)) 
    left = np.pad(image[:,:-1], ((0, 0), (1, 0)), constant_values=(0))
    return bot + top + right + left

def apply_threshold(image):
    return (image >= threshold) * image

def filter_by_neighbours(image):
    neighbours = get_neighbours(image)
    return (neighbours >= neighbour_threshold) * image 

def scale_by_running_total(image):
    global total_difference
    total_difference = np.add(total_difference, image)
    return (image / total_difference) * count

def filter_out_by_total(image):
    image = image * (total == 0)
    return image

def calc_frame_2(image, count, width, height):
    
    # return total 
    image = to_pixel_form(image)

    image = filter_out_by_total(image)
    # neigh_sum = get_sum_of_neighbours(image)
    # image = image + neigh_sum
    # image = apply_threshold(image)
    # image = filter_by_neighbours(image)
    image = scale_by_factor(image)

    image = from_pixel_form(image)

    return image

processer.run(calc_frame_2)
