import numpy as np

def angle_between_vectors(v1, v2):
    """Returns the angle in radians between vectors 'v1' and 'v2'"""
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def angular_velocity_between_vectors_radians(v1, v2, time_delta):
    """Returns the angular velocity in radians per second between vectors 'v1' and 'v2'"""
    angle = angle_between_vectors(v1, v2)
    return angle / time_delta

def angular_velocity_between_vectors_degrees(v1, v2, time_delta):
    """Returns the angular velocity in radians per second between vectors 'v1' and 'v2'"""
    angle = angle_between_vectors(v1, v2)
    return np.degrees(angle) / time_delta

