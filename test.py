
import numpy as np

def get_sum_of_neighbours(image):
    bot = np.pad(image[1:,:], ((0, 1), (0, 0)), constant_values=(0))
    top = np.pad(image[:-1,:], ((1, 0), (0, 0)), constant_values=(0))
    right = np.pad(image[:,1:], ((0, 0), (0, 1)), constant_values=(0)) 
    left = np.pad(image[:,:-1], ((0, 0), (1, 0)), constant_values=(0))
    return bot + top + right + left

def filter_by_non_empty_neighbours(image):
    neigh = get_sum_of_neighbours(image)
    image = image * (neigh > 0.1)
    return image

test_data = np.array(
  [[1, 1, 3],
   [0, 5, 0],
   [7, 0, 9]]
)
print(filter_by_non_empty_neighbours(test_data))
