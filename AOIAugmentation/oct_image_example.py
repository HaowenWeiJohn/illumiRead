import numpy as np
import cv2

# Load the image using Pillow
image_path = 'OCT_Image.png'
pil_image = cv2.imread(image_path)

# Convert the image to a NumPy array
numpy_array = np.array(pil_image)


image = np.imag()