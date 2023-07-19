from utils.DataProcessors import *
from utils.gaze_utils import GazeData, GazeType
from utils.general_utils import init_fifo_buffer_with_duration_sampling_rate, calculate_angular_dispersion, \
    edge_ignore_linear_interpolation, angular_velocity_between_vectors_degrees
from collections import deque


class GazeDataGapFilling(DataProcessor):

    def __init__(self, sampling_frequency=250,
                 max_gap_duration=75,
                 sampling_frequency_unit_duration_unit_scaling_factor=1000,
                 invalid_flag=0):
        super().__init__()
        self.sampling_frequency = sampling_frequency
        self.max_gap_duration = max_gap_duration
        self.sampling_frequency_unit_duration_unit_scaling_factor = sampling_frequency_unit_duration_unit_scaling_factor
        self.max_gap_duration_in_seconds = max_gap_duration / sampling_frequency_unit_duration_unit_scaling_factor
        self.buffer_size = int(sampling_frequency * (
                self.max_gap_duration / self.sampling_frequency_unit_duration_unit_scaling_factor))
        self.invalid_flag = invalid_flag

        self._gaze_data_buffer = deque(maxlen=int(self.buffer_size))

        # self.gap_holding = False
        self.gap_head = 0
        self.gap_holding = False
        self.gap_buffer_full = False
        self.a = 0

    def process_sample(self, gaze_data: GazeData):
        '''

        :param gaze_data:
        :return: gaze data
        '''
        # self.a+=1
        # print(self.a)
        # if self.a == 13869:
        #     pass
        # this is not filter with buffer, but just a gap filling # [ ->x x x x x] #
        self._gaze_data_buffer.appendleft(gaze_data)
        print(gaze_data.combined_eye_gaze_data.gaze_point_valid)

        if gaze_data.combined_eye_gaze_data.gaze_point_valid == 0:
            if self.gap_holding is False and self.gap_buffer_full is False:  # no gap in the buffer
                self.gap_holding = True
                self.gap_head += 1
            elif self.gap_buffer_full is True:  # if the gap buffer is full
                self.gap_head += 1
            elif self.gap_head + 1 == self.buffer_size:  # if the gap is already full which means the last
                self.gap_buffer_full = True
                self.gap_holding = False
                self.gap_head += 1
            else:
                self.gap_head += 1
        else:
            if self.gap_holding is True and self.gap_buffer_full is False:
                if self._gaze_data_buffer[self.gap_head + 1].combined_eye_gaze_data.gaze_point_valid == 1:
                    print('pad_gap' + str(self.gap_head + 1))
                self.gap_holding = False
                self.gap_head = 0
            elif self.gap_buffer_full is True:
                self.gap_buffer_full = False  # reset the gap buffer the new available valid data becomes the head
                self.gap_head = 0

        return self._gaze_data_buffer[-1]


class GazeFilterFixationDetectionIDTAngular(DataProcessor):
    def __init__(self,
                 sampling_frequency=250, duration=100,
                 sampling_frequency_unit_duration_unit_scaling_factor=1000,
                 angular_threshold_degree=1.2, dtype=np.float64):
        super().__init__()

        self.sampling_frequency = sampling_frequency
        self.duration = duration
        self.sampling_frequency_unit_duration_unit_scaling_factor = sampling_frequency_unit_duration_unit_scaling_factor
        self.angular_threshold_degree = angular_threshold_degree
        self.dtype = dtype

        self._gaze_data_buffer = None
        self.buffer_size = None
        self._gaze_vector_buffer = None

    def evoke_function(self):
        self.buffer_size = int(self.sampling_frequency * (
                self.duration / self.sampling_frequency_unit_duration_unit_scaling_factor))

        self._gaze_data_buffer = deque(maxlen=int(self.buffer_size))
        self._gaze_vector_buffer = deque(maxlen=int(self.buffer_size))

    def set_data_processor_params(self, sampling_frequency=250, duration=150,
                                  sampling_frequency_unit_duration_unit_scaling_factor=1000,
                                  angular_threshold_degree=1.5, dtype=np.float64):
        self.sampling_frequency = sampling_frequency
        self.duration = duration
        self.sampling_frequency_unit_duration_unit_scaling_factor = sampling_frequency_unit_duration_unit_scaling_factor
        self.angular_threshold_degree = angular_threshold_degree
        self.dtype = dtype

    def process_sample(self, gaze_data: GazeData):
        # centroid of the gaze data will be assigned
        self._gaze_data_buffer.appendleft(gaze_data)
        # self._gaze_vector_buffer.appendleft(gaze_data.combined_eye_gaze_data.gaze_direction)

        if gaze_data.combined_eye_gaze_data.gaze_point_valid:
            self._gaze_vector_buffer.appendleft(gaze_data.combined_eye_gaze_data.gaze_direction)
        else:
            # empty the buffer
            self._gaze_vector_buffer.clear()
            self._gaze_data_buffer.appendleft(gaze_data)

        if len(self._gaze_vector_buffer) == self.buffer_size:
            angular_dispersion = calculate_angular_dispersion(self._gaze_vector_buffer, self.dtype)
            if angular_dispersion <= self.angular_threshold_degree:
                gaze_data.gaze_type = GazeType.FIXATION
            else:
                gaze_data.gaze_type = GazeType.SACCADE
        else:
            gaze_data.gaze_type = GazeType.UNDETERMINED

        return gaze_data


class GazeFilterFixationDetectionIVT(DataProcessor):
    def __init__(self, angular_threshold_degree=100):
        super().__init__()
        self.last_gaze_data = GazeData()
        self.angular_threshold_degree = angular_threshold_degree


    def process_sample(self, gaze_data: GazeData):
        if self.last_gaze_data.combined_eye_gaze_data.gaze_point_valid:

            speed = angular_velocity_between_vectors_degrees(
                self.last_gaze_data.combined_eye_gaze_data.gaze_direction,
                gaze_data.combined_eye_gaze_data.gaze_direction,
                time_delta=gaze_data.timestamp - self.last_gaze_data.timestamp)
            # print(speed)
            if speed <= self.angular_threshold_degree:
                gaze_data.gaze_type = GazeType.FIXATION
            else:
                gaze_data.gaze_type = GazeType.SACCADE
        else:
            print('invalid gaze data')
        self.last_gaze_data = gaze_data

        return gaze_data

