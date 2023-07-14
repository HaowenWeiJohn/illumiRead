from utils.DataProcessors import *
from utils.general_utils import init_fifo_buffer_with_duration_sampling_rate, calculate_angular_dispersion, \
    TimeSensitiveCircularBufferFIFO


class GapFilling(DataProcessor):
    def __init__(self,
                 max_gap_duration=75,
                 duration_unit_to_second_scaling=1000,
                 missing_data_flag=0,
                 dtype=np.float64):
        super().__init__()
        self.max_gap_duration = max_gap_duration
        self.duration_unit_to_second_scaling = duration_unit_to_second_scaling
        self.missing_data_flag = missing_data_flag
        self.dtype = dtype

        self._gap_buffer = None

    def process_sample_timestamp(self, data, timestamp): # data -1 means missing data
        self._gap_buffer.push(data, timestamp)
        missing_data_flag_indices = self._gap_buffer.index(self.missing_data_flag)
        # TODO: implement the gap filling algorithm







        # 1. find the place with missing data

        # 2. check position of missing data


    def evoke_function(self):
        self._gap_buffer = TimeSensitiveCircularBufferFIFO(duration=self.max_gap_duration,
                                                           duration_unit_to_second_scaling=self.duration_unit_to_second_scaling,
                                                           dtype=np.float64)

    def set_data_processor_params(self, max_gap_duration=75,
                                  duration_unit_to_second_scaling=1000,
                                  dtype=np.float64):
        self.max_gap_duration = max_gap_duration
        self.duration_unit_to_second_scaling = duration_unit_to_second_scaling
        self.dtype = dtype

    def reset_data_processor(self):
        self._gap_buffer.reset_buffer()


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
                                                                                # x, y, z
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


if __name__ == '__main__':
    a = GapFilling()
