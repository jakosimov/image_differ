import numpy as np


def filter_by_neighbours(image):
    bot = np.pad(image[1:,:], ((0, 1), (0, 0)), constant_values=(0))
    top = np.pad(image[:-1,:], ((1, 0), (0, 0)), constant_values=(0))
    right = np.pad(image[:,1:], ((0, 0), (0, 1)), constant_values=(0)) 
    left = np.pad(image[:,:-1], ((0, 0), (1, 0)), constant_values=(0))
    return bot + top + right + left


test_data = np.array(
  [[1, 2, 3],
   [4, 5, 6],
   [7, 8, 9]]
)

print(filter_by_neighbours(test_data))
