import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load your RGB image
image_path = "../AOIAugmentation/OCT_Image.png"  # Replace with the actual path to your image
rgb_image = cv2.imread(image_path)

# Convert the RGB image to grayscale
gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)

# Threshold the grayscale image to create a binary mask
_, binary_mask = cv2.threshold(gray_image, 254, 1, cv2.THRESH_BINARY_INV)

# Invert the binary mask so that white pixels become 0 and colored pixels become 1
binary_mask = cv2.bitwise_not(binary_mask)

# Display the binary mask
cv2.imshow("Binary Mask", binary_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
