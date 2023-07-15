from utils.DataProcessors import *
from utils.general_utils import init_fifo_buffer_with_duration_sampling_rate, calculate_angular_dispersion, \
    edge_ignore_linear_interpolation


class GapFilling(DataProcessor):
    def __init__(self, sampling_frequency=250,
                 max_gap_duration=75,
                 sampling_frequency_unit_duration_unit_scaling_factor=1000,
                 missing_data_flag=0,
                 dtype=np.float64):
        super().__init__()

        self.sampling_frequency = sampling_frequency
        self.max_gap_duration = max_gap_duration
        self.sampling_frequency_unit_duration_unit_scaling_factor = sampling_frequency_unit_duration_unit_scaling_factor
        self.missing_data_flag = missing_data_flag
        self.dtype = dtype

        self._data_buffer = None
        self._valid_buffer = None

        self.gap_head = 0
        self.gap_holding = False
        self.gap_full = False

    def process_sample(self, data, valid):  # data -1 means missing data
        self._data_buffer.push(data)
        self._valid_buffer.push(valid)

        if not valid:
            if self.gap_head == 0 and not self.gap_holding:
                # find new gap
                self.gap_head += 1
                self.gap_holding = True

            elif self.gap_head == self._valid_buffer.buffer_size - 2:
                # gap full
                self.gap_full = True
            else:
                # gap not full
                self.gap_head += 1
        elif valid:
            # if valid data comes, gap not full, fill the gap
            if self.gap_holding and not self.gap_full:
                self._valid_buffer.buffer[1:self.gap_head + 1] = 1
                for channel in range(self.channel_num):
                    self._data_buffer.buffer[:, channel][0:self.gap_head + 2] = np.interp(
                        np.arange(self.gap_head + 2), [0, self.gap_head + 1],
                        [self._data_buffer.buffer[0, channel], self._data_buffer.buffer[self.gap_head + 1, channel]])

                self.gap_head = 0
                self.gap_holding = False

            elif self.gap_full:
                self.gap_head = 0
                self.gap_holding = False
                self.gap_full = False

            else:
                pass

        return self._data_buffer[-1], self._valid_buffer[-1]

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
        self._data_buffer.reset_buffer()
        self._valid_buffer.reset_buffer()


class GazeFilterFixationDetectionIDTAngular(DataProcessor):
    def __init__(self,
                 sampling_frequency=250, duration=150,
                 sampling_frequency_unit_duration_unit_scaling_factor=1000,
                 angular_threshold_degree=1.5, dtype=np.float64):
        super().__init__()

        self.sampling_frequency = sampling_frequency
        self.duration = duration
        self.sampling_frequency_unit_duration_unit_scaling_factor = sampling_frequency_unit_duration_unit_scaling_factor
        self.angular_threshold_degree = angular_threshold_degree

        self.dtype = dtype

        self._gaze_vector_buffer = None

    def evoke_function(self):
        self._gaze_vector_buffer = init_fifo_buffer_with_duration_sampling_rate(duration=self.duration,
                                                                                sampling_frequency=self.sampling_frequency,
                                                                                channel_number=self.channel_num,
                                                                                sampling_frequency_unit_duration_unit_scaling_factor=self.sampling_frequency_unit_duration_unit_scaling_factor,
                                                                                dtype=self.dtype)

    def set_data_processor_params(self, sampling_frequency=250, duration=150,
                                  sampling_frequency_unit_duration_unit_scaling_factor=1000,
                                  angular_threshold_degree=1.5, dtype=np.float64):

        self.sampling_frequency = sampling_frequency
        self.duration = duration
        self.sampling_frequency_unit_duration_unit_scaling_factor = sampling_frequency_unit_duration_unit_scaling_factor
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

# if __name__ == '__main__':
#     a = GapFilling()
