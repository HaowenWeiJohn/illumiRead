import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import sys

root_dir = 'D:/HaowenWei/PycharmProjects/brain-diffuser'
test_image = np.load(root_dir + '/data/processed_data/subj01/nsd_test_stim_sub1.npy').astype(np.uint8)
print(test_image.shape)

# save all images to the image_directory
image_directory= 'image_directory'
for i in range(test_image.shape[0]):
    # convert to BGR to RGB
    test_image[i] = cv2.cvtColor(test_image[i], cv2.COLOR_BGR2RGB)
    cv2.imwrite(os.path.join(image_directory, str(i) + '.png'), test_image[i])
