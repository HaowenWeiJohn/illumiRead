from utils.DataProcessors import *
from utils.gaze_utils import GazeData
from utils.general_utils import init_fifo_buffer_with_duration_sampling_rate, calculate_angular_dispersion, \
    edge_ignore_linear_interpolation
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
            if self.gap_holding is False and self.gap_buffer_full is False: # no gap in the buffer
                self.gap_holding = True
                self.gap_head += 1
            elif self.gap_buffer_full is True: # if the gap buffer is full
                self.gap_head += 1
            elif self.gap_head+1 == self.buffer_size: # if the gap is already full which means the last
                self.gap_buffer_full = True
                self.gap_holding = False
                self.gap_head += 1
            else:
                self.gap_head += 1
        else:
            if self.gap_holding is True and self.gap_buffer_full is False:
                if self._gaze_data_buffer[self.gap_head+1].combined_eye_gaze_data.gaze_point_valid == 1:
                    print('pad_gap' + str(self.gap_head+1))
                self.gap_holding = False
                self.gap_head = 0
            elif self.gap_buffer_full is True:
                self.gap_buffer_full = False # reset the gap buffer the new available valid data becomes the head
                self.gap_head = 0


        return self._gaze_data_buffer[-1]

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

        self.buffer_size = int(sampling_frequency * (
                self.duration / self.sampling_frequency_unit_duration_unit_scaling_factor))

        self._gaze_data_buffer = deque(maxlen=int(self.buffer_size))
    def set_data_processor_params(self, sampling_frequency=250, duration=150,
                                  sampling_frequency_unit_duration_unit_scaling_factor=1000,
                                  angular_threshold_degree=1.5, dtype=np.float64):

        self.sampling_frequency = sampling_frequency
        self.duration = duration
        self.sampling_frequency_unit_duration_unit_scaling_factor = sampling_frequency_unit_duration_unit_scaling_factor
        self.angular_threshold_degree = angular_threshold_degree
        self.dtype = dtype

    def process_sample(self, gaze_data: GazeData):
        pass
        # self._gaze_vector_buffer.push(gaze_vector)
        # if self._gaze_vector_buffer.is_full():
        #     dispersion = calculate_angular_dispersion(self._gaze_vector_buffer.buffer)
        #     if dispersion < self.angular_threshold_degree:
        #         return True
        # return False

    def reset_data_processor(self):
        self._gaze_vector_buffer.reset_buffer()




        # if gaze_data.combined_eye_gaze_data.gaze_point_valid is False:
        #     # if self.gap_holding is False
        # #     if self.gap_holding is False:
        # #         self.gap_holding = True
        # #         self.gap_head += 1
        # #     elif self.gap_head == self.buffer_size:
        # #         self.gap_buffer_full = True
        # #         self.gap_head = 0
        # #         self.gap_holding = False
        # #     else:
        # #         self.gap_head += 1
        # # else:
        # #     if self.gap_holding is True:
        # #         # padding the gap
        # #         self.gap_holding = False
        # #         self.gap_head = 0
        # #     else:
        # #         pass

        #
        # if gaze_data.combined_eye_gaze_data.gaze_point_valid is False:  # if invalid
        #     # if self.gap_head == -1:
        #     #     self.gap_head += 1
        #     # else:
        #     self.gap_head += 1
        #
        # else:
        #     if self.gap_head != -1:
        #         pass
        #
        # # gaze_data_return = self.pop_overflow_gaze_data()
        # return gaze_data_return

    # def pop_overflow_gaze_data(self):
    #     over_flow_gaze_data = []
    #     if self._gaze_data_buffer[0] - self._gaze_data_buffer[-1] > self.max_gap_duration_in_seconds:
    #         over_flow_gaze_data.append(self._gaze_data_buffer.pop())
    #     return over_flow_gaze_data
