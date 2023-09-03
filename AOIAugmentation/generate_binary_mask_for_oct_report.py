import cv2
import numpy as np
from utils.cv_utils import generate_image_binary_mask, generate_attention_grid_mask
import matplotlib.pyplot as plt

image_height = 1000
image_width = 2000
attention_patch_shape = np.array([20,20])

image_path = 'OCT_Image.png'
image = cv2.imread(image_path)

image = cv2.resize(image, (image_width, image_height))


binary_mask = generate_image_binary_mask(image)

attention_grid_mask = generate_attention_grid_mask(binary_mask, attention_patch_shape=attention_patch_shape)

plt.imshow(attention_grid_mask)
plt.show()

