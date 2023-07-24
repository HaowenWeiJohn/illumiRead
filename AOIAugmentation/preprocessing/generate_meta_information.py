import cv2
import numpy as np
from utils.cv_utils import generate_iamge_binary_mask, generate_attention_grid_mask
from matplotlib import pyplot as plt
image_height = 500
image_width = 1000
attention_patch_size = np.array([20,20])

image_path = 'OCT_Image.png'
image = cv2.imread(image_path)

image = cv2.resize(image, (image_width, image_height))


binary_mask = generate_iamge_binary_mask(image)

attention_grid_mask = generate_attention_grid_mask(binary_mask, attention_patch_shape=attention_patch_size)



