import numpy as np
import processer
import sys

file_name = sys.argv[1]

input_file = 'diff_' + file_name + '.avi'
output_file = 'out_' + file_name + '.avi'
emphasis_factor = 100.0
threshold = 2
neighbour_threshold = 10


processer = processer.Processer(input_file, output_file, max_count=-1)
width = processer.width
height = processer.height

# total_difference = np.full((width, height), 1) 

print('width =', width)
print('height =', height)

def get_sum_of_neighbours(image):
    bot = np.pad(image[1:,:], ((0, 1), (0, 0)), constant_values=(0))
    top = np.pad(image[:-1,:], ((1, 0), (0, 0)), constant_values=(0))
    right = np.pad(image[:,1:], ((0, 0), (0, 1)), constant_values=(0)) 
    left = np.pad(image[:,:-1], ((0, 0), (1, 0)), constant_values=(0))
    return bot + top + right + left

def calc_frame_2(image, count, width, height, videoWriter):
    global total_difference
    image = np.uint32(image)

    # image = np.mean(image, 2)
    image = (image[:,:,0] + image[:,:,1] + image[:,:,2]) / 3
    image = (image >= threshold) * image

    # total_difference = np.add(total_difference, image)

    neighbours = get_neighbours(image)
    image = (neighbours >= neighbour_threshold) * image 

    # image = (image / total_difference) * count

    image = image * emphasis_factor
    image = np.minimum(image, 255)
    image = np.repeat(image, 3)
    image = np.resize(image, (width, height, 3))

    image = np.uint8(image)
    videoWriter.write(image)

processer.run(calc_frame_2)
