import cv2
import numpy as np
import torch
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt


image_height = 1000
image_width = 2000

# image_shape = np.array([1000, 2000, 3])
attention_patch_shape = np.array([20, 20])

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
image = cv2.imread(r"../AOIAugmentation/OCT_Image.png")
image = cv2.resize(image, (image_width, image_height))


image = np.moveaxis(image, -1, 0)


image = torch.tensor(image, dtype=torch.float32, device=device)
kernel = torch.tensor(np.ones(shape=(3,attention_patch_shape[0], attention_patch_shape[1])), dtype=torch.float32, device=device)

attention_grid = F.conv2d(input=image.view(1, image.shape[0], image.shape[1], image.shape[2]),
                          weight=kernel.view(1, kernel.shape[0], kernel.shape[1], kernel.shape[2]),
                          stride=(attention_patch_shape[0], attention_patch_shape[1]))

# create attention grid from

print(attention_grid.shape)













# Assuming you have an RGB image as a 3-channel tensor of shape (batch_size, channels, height, width)
# and a kernel as a 3-dimensional tensor of shape (out_channels, in_channels, kernel_size, kernel_size)
# where out_channels and in_channels correspond to the number of input and output channels respectively.

# # Example RGB image of shape (1, 3, 32, 32)
# batch_size = 1
# channels = 3
# height = 32
# width = 32
# rgb_image = torch.rand(batch_size, channels, height, width)
#
# # Example kernel of shape (4, 3, 5, 5)
# out_channels = 1
# kernel_size = 5
# kernel = torch.rand(out_channels, channels, kernel_size, kernel_size)
#
# # Perform convolution
# output = F.conv2d(rgb_image, kernel, padding=kernel_size // 2)  # Add padding to keep the output size the same
#
# # The output will be a tensor of shape (batch_size, out_channels, height, width)
# print(output.shape)

