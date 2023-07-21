from utils.attention_utils import get_ave_attention
import numpy as np
patch_shape = (20,20)
image_shape = (1000,2000)
attention_matrix = np.random.random((5000, 5000))

ave_attention_image = get_ave_attention(patch_shape=patch_shape, image_shape=image_shape, attention_matrix=attention_matrix)



