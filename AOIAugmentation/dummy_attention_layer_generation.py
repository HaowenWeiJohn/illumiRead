import numpy as np

from utils.general_utils import patch_index_to_attention_index

image_width = 2000
image_height = 1000
patch_shape = (20, 20)



patch_num = int((image_width/patch_shape[0]) * (image_height/patch_shape[1]))
# print(patch_num)

attention_matrix = np.random.random((patch_num, patch_num))

# attention_matrix = np.where(attention_matrix)

current_patch_index = (45, 73)
patch_size = (50,100)

patch_flattened_index = patch_index_to_attention_index(current_patch_index, patch_size)
target_attention = attention_matrix[:, patch_flattened_index]









