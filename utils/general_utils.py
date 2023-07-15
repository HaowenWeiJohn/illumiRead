import numpy as np
from collections import deque
from itertools import combinations


# class DataProcessorDeque(deque):
#     """A deque that can be used as a data processor"""
#     def __init__(self, maxlen=None, channel_num=1, initial_value=0):
#         super().__init__(maxlen=maxlen)
#         self.channel_num = channel_num
#         self.initial_value = initial_value
#

# class CircularBuffer1: # (frame_len, maxlen)
#     def __init__(self, buffer_size, frame_size ,dtype=np.float64, fill_value=0): # self, num_frames, frame_size, fill_value=0, dtype=np.float64
#         self.buffer_size = buffer_size
#         self.frame_size = frame_size
#         self.buffer = np.full((self.buffer_size, self.frame_size), dtype=dtype, fill_value=fill_value)
#         self.head = 0
#         self.tail = 0
#         self.full = False
#
#     def is_empty(self):
#         return not self.full and self.head == self.tail
#
#     def is_full(self):
#         return self.full
#
#     def enqueue(self, item):
#         self.buffer[self.head] = item
#         self.head = (self.head + 1) % self.buffer_size
#         if self.head == self.tail:
#             self.full = True
#             self.tail = (self.tail + 1) % self.buffer_size
#
#     def dequeue(self):
#         if self.is_empty():
#             raise IndexError("Circular buffer is empty")
#         item = self.buffer[self.tail]
#         self.full = False
#         self.tail = (self.tail + 1) % self.buffer_size
#         return item
#
#     def __len__(self):
#         if self.full:
#             return self.buffer_size
#         elif self.head >= self.tail:
#             return self.head - self.tail
#         else:
#             return self.buffer_size - (self.tail - self.head)
#
#     def __getitem__(self, index):
#         if index < 0 or index >= len(self):
#             raise IndexError("Circular buffer index out of range")
#         return self.buffer[(self.tail + index) % self.buffer_size]


class CircularBufferFIFO:
    def __init__(self, buffer_size, frame_size, fill_value=0, dtype=np.float64):
        self.buffer_size = buffer_size
        self.frame_size = frame_size
        self.fill_value = fill_value
        self.dtype = dtype
        self.buffer = np.full((buffer_size, frame_size), fill_value=fill_value, dtype=self.dtype)
        self.head = 0

    def push(self, new_frame):
        # Shift the existing frames to the right
        self.buffer = np.roll(self.buffer, 1, axis=0)
        # Update the first column with the new frame
        self.buffer[0] = new_frame
        # print(f"{a = } when {b = }")
        if self.head < self.buffer_size:
            self.head += 1

    def pop(self):
        # Shift the existing frames to the left
        if self.head > 0:
            self.head -= 1
            self.buffer = np.roll(self.buffer, -1, axis=0)
            return self.buffer[-1]

    def last(self):
        if not self.is_empty():
            return self.buffer[self.head - 1]

    def first(self):
        if not self.is_empty():
            return self.buffer[0]

    def __getitem__(self, index):
        return self.buffer[index]

    def get_all(self):
        return self.buffer[:self.head]

    def is_full(self):
        return self.head == self.buffer_size

    def is_empty(self):
        return self.head == 0

    def reset_buffer(self):
        self.buffer = np.full((self.buffer_size, self.frame_size), fill_value=self.fill_value, dtype=self.dtype)
        self.head = 0


# class TimeSensitiveCircularBufferFIFO:  # duration in milliseconds by default
#     """Returns a time sensitive circular buffer FIFO"""
#
#     def __init__(self, duration, duration_unit_to_second_scaling=1000, dtype=np.float64):
#         self.duration = duration
#         self.duration_unit_to_second_scaling = duration_unit_to_second_scaling
#         self.dtype = dtype
#
#         self.duration_in_second = self.duration / self.duration_unit_to_second_scaling
#         self.data_buffer = deque()
#         self.timestamp_buffer = deque()
#
#         self.data_return_buffer = deque()
#         self.timestamp_return_buffer = deque()
#
#     def push(self, data, timestamp):
#         self.data_buffer.appendleft(data)
#         self.timestamp_buffer.appendleft(timestamp)
#
#         return self.collect_overflow_data()
#
#
#     def collect_overflow_data(self):
#         # recursively pop the oldest data until the buffer is not full
#         self.data_return_buffer.clear()
#         self.timestamp_return_buffer.clear()
#
#         while self.is_full():
#             self.timestamp_return_buffer.appendleft(self.timestamp_buffer.pop())
#             self.data_return_buffer.appendleft(self.data_buffer.pop())
#
#         return self.data_return_buffer, self.timestamp_return_buffer
#
#
#
#
#     def pop(self):
#         if not self.is_empty():
#             return self.data_buffer.pop(), self.timestamp_buffer.pop()
#         else:
#             return None, None
#
#     def is_full(self):
#         return self.timestamp_buffer[-1] - self.timestamp_buffer[
#             0] > self.duration_in_second  # the buffer is full, need pop
#
#     def first(self):
#         return self.data_buffer[0], self.timestamp_buffer[0]
#
#     def last(self):
#         return self.data_buffer[-1], self.timestamp_buffer[-1]
#
#     def is_empty(self):
#         return len(self.data_buffer) == 0
#
#     def reset_buffer(self):
#         self.data_buffer = deque()
#         self.timestamp_buffer = deque()


# class TimeSensitiveCircularBufferWithValidation:  # duration in milliseconds by default
#     """Returns a time sensitive circular buffer FIFO"""
#
#     def __init__(self, duration, duration_unit_to_second_scaling=1000, dtype=np.float64):
#         self.duration = duration
#         self.duration_unit_to_second_scaling = duration_unit_to_second_scaling
#         self.dtype = dtype
#
#         self.duration_in_second = self.duration / self.duration_unit_to_second_scaling
#         self.data_buffer = deque()
#         self.valid_buffer = deque()
#         self.timestamp_buffer = deque()
#
#         self.data_return_buffer = deque()
#         self.valid_return_buffer = deque()
#         self.timestamp_return_buffer = deque()
#
#     def push(self, data, valid, timestamp):
#         self.data_buffer.appendleft(data)
#         self.valid_buffer.appendleft(valid)
#         self.timestamp_buffer.appendleft(timestamp)
#
#         return self.collect_overflow_data()
#
#     def gap_fill(self):
#         # find the gap
#         # fill the gap with the last valid data
#         # invalid_index = np.where(self.valid_buffer == False)[0]
#         # if len(invalid_index) > 0:
#         # finish the gap fill
#         pass
#
#
#     def collect_overflow_data(self):
#         # recursively pop the oldest data until the buffer is not full
#         self.data_return_buffer.clear()
#         self.valid_return_buffer.clear()
#         self.timestamp_return_buffer.clear()
#
#         while self.is_full():
#             self.timestamp_return_buffer.appendleft(self.timestamp_buffer.pop())
#             self.valid_return_buffer.appendleft(self.valid_return_buffer.pop())
#             self.data_return_buffer.appendleft(self.data_buffer.pop())
#
#         return self.data_return_buffer, self.valid_return_buffer,self.timestamp_return_buffer
#
#
#
#
#     def pop(self):
#         if not self.is_empty():
#             return self.data_buffer.pop(), self.timestamp_buffer.pop()
#         else:
#             return None, None
#
#     def is_full(self):
#         return self.timestamp_buffer[-1] - self.timestamp_buffer[
#             0] > self.duration_in_second  # the buffer is full, need pop
#
#     def first(self):
#         return self.data_buffer[0], self.timestamp_buffer[0]
#
#     def last(self):
#         return self.data_buffer[-1], self.timestamp_buffer[-1]
#
#     def is_empty(self):
#         return len(self.data_buffer) == 0
#
#     def reset_buffer(self):
#         self.data_buffer = deque()
#         self.timestamp_buffer = deque()


def init_fifo_buffer_with_duration_sampling_rate(duration, sampling_frequency, channel_number,
                                                 sampling_frequency_unit_duration_unit_scaling_factor=1,
                                                 fill_value=0, dtype=np.float64) -> CircularBufferFIFO:
    """Returns a tap initialization array with the specified duration, sampling frequency, channel number and fill value"""
    buffer_size = sampling_frequency * (
            duration / sampling_frequency_unit_duration_unit_scaling_factor)  # int(duration * sampling_frequency * sampling_frequency_duration_unit_scaling_factor)
    buffer_size = np.round(buffer_size).astype(int)
    return CircularBufferFIFO(buffer_size=buffer_size, frame_size=channel_number, fill_value=fill_value, dtype=dtype)


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


def edge_ignore_linear_interpolation(data, valid, invalid_flag=0, channel_number=3):
    valid_indexes = np.where(valid != invalid_flag)[0]
    valid[valid_indexes[0]:valid_indexes[-1] + 1] = 1  # set all valid to 1 in this range
    edge_ignored_values = data[valid_indexes]

    for channel in range(channel_number):

        interpolated_values = np.interp(np.arange(valid_indexes[-1] - valid_indexes[0] + 1),
                                        valid_indexes - valid_indexes[0], edge_ignored_values[:, channel])
        data[:, channel][valid_indexes[0]:valid_indexes[-1] + 1] = interpolated_values

    return data, valid


# def calculate_dispersion(unit_vectors, axis=0):
#     angles = []
#
#     # Calculate angles between unit vectors
#     for i in range(len(unit_vectors) - 1):
#         for j in range(i + 1, len(unit_vectors)):
#             dot_product = np.dot(unit_vectors[i], unit_vectors[j])
#             angle = np.arccos(dot_product)
#             angles.append(angle)
#         if len(angles) == 693:
#             pass
#
#     # Calculate dispersion
#     mean_angle = np.mean(angles)
#     squared_diff_sum = np.sum((angle - mean_angle) ** 2 for angle in angles)
#     variance = squared_diff_sum / len(angles)
#     dispersion = np.sqrt(variance)
#
#     return dispersion


import numpy as np
from itertools import combinations


def calculate_angular_dispersion(unit_vectors, in_degrees=True):
    angles = []

    # Calculate angles between unit vectors
    for vec1, vec2 in combinations(unit_vectors, 2):

        dot_product = np.dot(vec1, vec2)
        if dot_product > 1 or dot_product < -1:
            angle = 0
        else:
            angle = np.arccos(dot_product)
        angles.append(angle)

    # Calculate dispersion
    mean_angle = np.mean(angles)
    squared_diff_sum = np.sum((angle - mean_angle) ** 2 for angle in angles)
    variance = squared_diff_sum / len(angles)
    dispersion = np.sqrt(variance)

    dispersion = np.degrees(dispersion) if in_degrees else dispersion

    return dispersion
