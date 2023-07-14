from utils.DataProcessors import *
from utils.general_utils import init_fifo_buffer_with_duration_sampling_rate, calculate_angular_dispersion


class GapFilling(DataProcessor):
    def __init__(self,
                 sampling_frequency=250,
                 max_gap_duration=75,
                 sampling_frequency_unit_duration_unit_scaling_factor=1000,
                 missing_data_flag=0,
                 dtype=np.float64):
        super().__init__()
        self.sampling_frequency = sampling_frequency,
        self.max_gap_duration = max_gap_duration
        self.sampling_frequency_unit_duration_unit_scaling_factor = sampling_frequency_unit_duration_unit_scaling_factor
        self.missing_data_flag = missing_data_flag
        self.dtype = dtype

        self._data_buffer = None
        self._valid_buffer = None

    def process_sample(self, data, valid):  # data -1 means missing data

        return data, valid

    def evoke_function(self):
        self._data_buffer = init_fifo_buffer_with_duration_sampling_rate(duration=self.max_gap_duration,
                                                                         sampling_frequency=self.sampling_frequency,
                                                                         channel_number=self.channel_num,
                                                                         sampling_frequency_unit_duration_unit_scaling_factor=self.sampling_frequency_unit_duration_unit_scaling_factor,
                                                                         dtype=self.dtype)

        self._valid_buffer = init_fifo_buffer_with_duration_sampling_rate(duration=self.max_gap_duration,
                                                                          sampling_frequency=self.sampling_frequency,
                                                                          channel_number=1,
                                                                          sampling_frequency_unit_duration_unit_scaling_factor=self.sampling_frequency_unit_duration_unit_scaling_factor,
                                                                          dtype=self.dtype)

    def set_data_processor_params(self,
                                  sampling_frequency=250,
                                  max_gap_duration=75,
                                  duration_unit_to_second_scaling=1000,
                                  dtype=np.float64):

        self.sampling_frequency = sampling_frequency
        self.max_gap_duration = max_gap_duration
        self.duration_unit_to_second_scaling = duration_unit_to_second_scaling
        self.dtype = dtype

    def reset_data_processor(self):
        pass


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
                                                                                channel_number=self.channel_num,
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

    def process_sample(self, gaze_vector, valid, timestamp):
        self._gaze_vector_buffer.push(gaze_vector)
        if self._gaze_vector_buffer.is_full():
            dispersion = calculate_angular_dispersion(self._gaze_vector_buffer.buffer)
            if dispersion < self.angular_threshold_degree:
                return True
        return False

    def reset_data_processor(self):
        self._gaze_vector_buffer.reset_buffer()


if __name__ == '__main__':
    a = GapFilling()
