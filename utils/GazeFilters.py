from utils.DataProcessors import *
from utils.general_utils import init_fifo_buffer, calculate_angular_dispersion


class GazeFilterFixationDetectionIDTAngular(DataProcessor):
    def __init__(self,
                 sampling_frequency=250, duration=150,
                 sampling_frequency_duration_unit_scaling_factor=1000, angular_threshold_degree=1.5, dtype=np.float64):
        super().__init__()
        self.sampling_frequency = sampling_frequency
        self.duration = duration
        self.sampling_frequency_duration_unit_scaling_factor = sampling_frequency_duration_unit_scaling_factor
        self.angular_threshold_degree = angular_threshold_degree
        self.dtype = dtype

        self.gaze_vector_buffer = None

    def evoke_function(self):
        self.gaze_vector_buffer = init_fifo_buffer(duration=self.duration,
                                                   sampling_frequency=self.sampling_frequency,
                                                   channel_number=3,  # x, y, z
                                                   sampling_frequency_duration_unit_scaling_factor=self.sampling_frequency_duration_unit_scaling_factor,
                                                   dtype=self.dtype)

    def process_sample(self, gaze_vector):
        self.gaze_vector_buffer.push(gaze_vector)
        if self.gaze_vector_buffer.is_full():
            dispersion = calculate_angular_dispersion(self.gaze_vector_buffer.buffer)
            if dispersion < self.angular_threshold_degree:
                return True
        return False

    def reset_data_processor(self):
        self.gaze_vector_buffer.reset_buffer()