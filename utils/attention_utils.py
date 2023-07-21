import numpy as np


def patch_index_to_attention_index(patch_index, patch_size):
    flattened_index = np.ravel_multi_index(patch_index, patch_size)
    return flattened_index


def get_patch_image_size(patch_shape, image_shape):
    return np.array((image_shape[0] / patch_shape[0], image_shape[1] / patch_shape[1]), dtype=np.integer)


def get_ave_attention(patch_shape, image_shape, attention_matrix):
    patch_image_size = get_patch_image_size(patch_shape=patch_shape, image_shape=image_shape)
    ave_attention = np.average(attention_matrix, axis=1)
    ave_attention = np.reshape(ave_attention, newshape=patch_image_size)
    return ave_attention

