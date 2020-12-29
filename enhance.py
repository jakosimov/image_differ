import numpy as np
import processer

FPS = 20
max_count = -1
input_file = 'diff.avi'
output_file = 'output.avi'
emphasis_factor = 20.0
threshold = 1


processer = processer.Processer(input_file, output_file, FPS, max_count)
width = processer.width
height = processer.height

# total_difference = np.full((width, height, 3), 0) 

print('width =', width)
print('height =', height)

def calc_frame_2(image, count, width, height, videoWriter):
    image = np.uint32(image)
    # total_difference = np.add(total_difference, image)


    # image = np.mean(image, 2)
    image = (image[:,:,0] + image[:,:,1] + image[:,:,2]) / 3
    image = (image >= threshold) * image * emphasis_factor
    image = np.minimum(image, 255)
    image = np.repeat(image, 3)
    image = np.resize(image, (width, height, 3))

    image = np.uint8(image)
    videoWriter.write(image)

processer.run(calc_frame_2)
