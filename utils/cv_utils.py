import numpy as np
import matplotlib.pyplot as plt
import cv2
import torch
from PIL import Image, ImageDraw
import torch.nn.functional as F


def generate_iamge_binary_mask(image, depth_first=False):
    if depth_first:
        image = np.moveaxis(image, 0, -1)

    # Convert the RGB image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_mask = cv2.threshold(gray_image, 254, 1, cv2.THRESH_BINARY_INV)
    return binary_mask


def draw_grids_on_image(image_path, image_save_path, n, m):
    # Load the image
    img = Image.open(image_path)

    # Get image dimensions
    width, height = img.size

    # Calculate grid cell size
    cell_width = width // n
    cell_height = height // m

    # Create a drawing object
    draw = ImageDraw.Draw(img)

    # Draw vertical grid lines
    for x in range(0, width, cell_width):
        draw.line([(x, 0), (x, height)], fill=(0, 0, 0), width=1)

    # Draw horizontal grid lines
    for y in range(0, height, cell_height):
        draw.line([(0, y), (width, y)], fill=(0, 0, 0), width=1)

    # Save the modified image
    img.save(image_save_path)


def generate_attention_grid_mask(image_mask, attention_patch_shape):
    kernel = torch.tensor(np.ones(shape=(attention_patch_shape[0], attention_patch_shape[1])), dtype=torch.float32)
    image_mask = torch.tensor(image_mask, dtype=torch.float32)

    attention_grid_mask = F.conv2d(input=image_mask.view(1, 1, image_mask.shape[0], image_mask.shape[1]),
                                   weight=kernel.view(1, 1, attention_patch_shape[0], attention_patch_shape[1]),
                                   stride=(attention_patch_shape[0], attention_patch_shape[1]))

    attention_grid_mask = attention_grid_mask.squeeze().cpu().numpy()
    attention_grid_mask = np.where(attention_grid_mask > 0, 1, 0)
    return attention_grid_mask
