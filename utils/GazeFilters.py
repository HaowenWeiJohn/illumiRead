from utils.DataProcessors import *
from utils.general_utils import init_fifo_buffer_with_duration_sampling_rate, calculate_angular_dispersion


class GapFilling(DataProcessor):
    def __init__(self,
                 sampling_frequency=250,
                 max_gap_duration=75,
                 sampling_frequency_duration_unit_scaling_factor=1000,
                 dtype=np.float64):

        super().__init__()
        self.sampling_frequency = sampling_frequency
        self.max_gap_duration = max_gap_duration
        self.sampling_frequency_duration_unit_scaling_factor = sampling_frequency_duration_unit_scaling_factor
        self.dtype = dtype

        self.last_gaze_vector = None # x, y, z
        self.last_timestamp = None

    def evoke_function(self):
        self.last_gaze_vector = np.zeros(self.channel_num, dtype=self.dtype)
        self.last_timestamp = 0





class GazeFilterFixationDetectionIDTAngular(DataProcessor):
    def __init__(self,
                 sampling_frequency=250, duration=150,
                 sampling_frequency_duration_unit_scaling_factor=1000,

                 angular_threshold_degree=1.5, dtype=np.float64):
        super().__init__()
        self.sampling_frequency = sampling_frequency
        self.duration = duration
        self.sampling_frequency_duration_unit_scaling_factor = sampling_frequency_duration_unit_scaling_factor
        self.angular_threshold_degree = angular_threshold_degree
        self.dtype = dtype

        self._gaze_vector_buffer = None

    def evoke_function(self):
        self._gaze_vector_buffer = init_fifo_buffer_with_duration_sampling_rate(duration=self.duration,
                                                                                sampling_frequency=self.sampling_frequency,
                                                                                channel_number=self.channel_num,  # x, y, z
                                                                                sampling_frequency_duration_unit_scaling_factor=self.sampling_frequency_duration_unit_scaling_factor,
                                                                                dtype=self.dtype)


    def set_data_processor_params(self, sampling_frequency=250, duration=150,
                                  sampling_frequency_duration_unit_scaling_factor=1000,
                                  angular_threshold_degree=1.5, dtype=np.float64):

        self.sampling_frequency = sampling_frequency
        self.duration = duration
        self.sampling_frequency_duration_unit_scaling_factor = sampling_frequency_duration_unit_scaling_factor
        self.angular_threshold_degree = angular_threshold_degree
        self.dtype = dtype

    def process_sample(self, gaze_vector):
        self._gaze_vector_buffer.push(gaze_vector)
        if self._gaze_vector_buffer.is_full():
            dispersion = calculate_angular_dispersion(self._gaze_vector_buffer.buffer)
            if dispersion < self.angular_threshold_degree:
                return True
        return False

    def reset_data_processor(self):
        self._gaze_vector_buffer.reset_buffer()
