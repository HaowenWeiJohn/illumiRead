import pickle
import matplotlib.pyplot as plt
import numpy as np
from examples.TobiiEyeTrackerConfig import TobiiProFusionChannel
from utils.gaze_utils import EyeData, GazeData
from utils.general_utils import angle_between_vectors, angular_velocity_between_vectors_radians, \
    angular_velocity_between_vectors_degrees, init_fifo_buffer_with_duration_sampling_rate, calculate_angular_dispersion

file_path = 'TobiiGazeData.pickle'
# Open the file in binary mode
with open(file_path, 'rb') as file:
    # Load the data from the file
    gaze_raw = pickle.load(file)

gaze_data = gaze_raw['TobiiProFusionUnityLSLOutlet'][0]
timestamps = gaze_raw['TobiiProFusionUnityLSLOutlet'][1]

# invalid label


# left_eye_gaze_origin_valid = gaze_data[TobiiProFusionChannel.LeftGazeOriginValid]
# left_eye_gaze_point_valid = gaze_data[TobiiProFusionChannel.LeftGazePointValid]
# left_eye_pupil_diameter_valid = gaze_data[TobiiProFusionChannel.LeftPupilDiameterValid]
#
# right_eye_gaze_origin_valid = gaze_data[TobiiProFusionChannel.RightGazeOriginValid]
# right_eye_gaze_point_valid = gaze_data[TobiiProFusionChannel.RightGazePointValid]
# right_eye_pupil_diameter_valid = gaze_data[TobiiProFusionChannel.RightPupilDiameterValid]
#
# left_eye_on_display_area_x = gaze_data[TobiiProFusionChannel.LeftGazePointOnDisplayAreaX]
# left_eye_on_display_area_y = gaze_data[TobiiProFusionChannel.LeftGazePointOnDisplayAreaY]

# plt.plot(left_eye_on_display_area_x[0:1500], left_eye_on_display_area_y[0:1500])
# plt.xlim(0, 1)
# plt.ylim(0, 1)
# plt.show()

# gap filling
# test IDT example


sampling_frequency = 250.0
# while there are still point
sampling_frequency_unit_duration_unit_scaling_factor = 1000  # millisecond
max_gap_duration = 75  # millisecond
# gap_fill_check_buffer_size = sampling_frequency * (
#             max_gap_duration / sampling_frequency_unit_duration_unit_scaling_factor)  # 75 ms
angular_velocity_limit_degree = 1000  # degree per second

buffer_duration = 150  # millisecond

# gap_filling_filter = GapFilling(sampling_frequency=sampling_frequency,
#                                 max_gap_duration=max_gap_duration,
#                                 sampling_frequency_unit_duration_unit_scaling_factor=sampling_frequency_unit_duration_unit_scaling_factor,
#                                 missing_data_flag=0,
#                                 dtype=np.float64)
# gap_filling_filter.set_channel_num(5)
# gap_filling_filter.evoke_data_processor()

# gaze_vector_buffer = init_fifo_buffer_with_duration_sampling_rate(duration=buffer_duration, sampling_frequency=sampling_frequency, channel_number=3,
#                                                                   sampling_frequency_unit_duration_unit_scaling_factor=sampling_frequency_unit_duration_unit_scaling_factor,
#                                                                   fill_value=0, dtype=np.float64)

last_timestamp = 0
last_combined_gaze_vector_normalized = np.array([0, 0, 1])

for index, timestamp in enumerate(timestamps):
    gaze_data_t = gaze_data[:, index]

    # left_eye_gaze_point_valid = gaze_data_t[TobiiProFusionChannel.LeftGazePointValid]
    # right_eye_gaze_point_valid = gaze_data_t[TobiiProFusionChannel.RightGazePointValid]

    left_gaze_origin_in_user_coordinate = gaze_data_t[[TobiiProFusionChannel.LeftGazeOriginInUserCoordinatesX,
                                                       TobiiProFusionChannel.LeftGazeOriginInUserCoordinatesY,
                                                       TobiiProFusionChannel.LeftGazeOriginInUserCoordinatesZ]]

    left_gaze_point_in_user_coordinate = gaze_data_t[[TobiiProFusionChannel.LeftGazePointInUserCoordinatesX,
                                                      TobiiProFusionChannel.LeftGazePointInUserCoordinatesY,
                                                      TobiiProFusionChannel.LeftGazePointInUserCoordinatesZ]]

    left_gaze_origin_in_track_box_coordinate = gaze_data_t[
        [TobiiProFusionChannel.LeftGazeOriginInTrackBoxCoordinatesX,
         TobiiProFusionChannel.LeftGazeOriginInTrackBoxCoordinatesY,
         TobiiProFusionChannel.LeftGazeOriginInTrackBoxCoordinatesZ]]

    left_gaze_origin_valid = gaze_data_t[TobiiProFusionChannel.LeftGazeOriginValid]
    left_gaze_point_valid = gaze_data_t[TobiiProFusionChannel.LeftGazePointValid]

    left_pupil_diameter = gaze_data_t[TobiiProFusionChannel.LeftPupilDiameter]
    left_pupil_diameter_valid = gaze_data_t[TobiiProFusionChannel.LeftPupilDiameterValid]

    left_gaze_point_on_display_area = gaze_data_t[
        [TobiiProFusionChannel.LeftGazePointOnDisplayAreaX, TobiiProFusionChannel.LeftGazePointOnDisplayAreaY]]

    left_eye_gaze_data = EyeData(gaze_origin_in_user_coordinate=left_gaze_origin_in_user_coordinate,
                                 gaze_point_in_user_coordinate=left_gaze_point_in_user_coordinate,
                                 gaze_origin_valid=left_gaze_origin_valid,
                                 gaze_point_valid=left_gaze_point_valid,
                                 gaze_origin_in_trackbox_coordinate=left_gaze_origin_in_track_box_coordinate,
                                 pupil_diameter=left_pupil_diameter,
                                 pupil_diameter_valid=left_pupil_diameter_valid,
                                 gaze_point_on_display_area=left_gaze_point_on_display_area,
                                 timestamp=timestamp)

    right_gaze_origin_in_user_coordinate = gaze_data_t[[TobiiProFusionChannel.RightGazeOriginInUserCoordinatesX,
                                                        TobiiProFusionChannel.RightGazeOriginInUserCoordinatesY,
                                                        TobiiProFusionChannel.RightGazeOriginInUserCoordinatesZ]]

    right_gaze_point_in_user_coordinate = gaze_data_t[[TobiiProFusionChannel.RightGazePointInUserCoordinatesX,
                                                       TobiiProFusionChannel.RightGazePointInUserCoordinatesY,
                                                       TobiiProFusionChannel.RightGazePointInUserCoordinatesZ]]

    right_gaze_origin_in_track_box_coordinate = gaze_data_t[
        [TobiiProFusionChannel.RightGazeOriginInTrackBoxCoordinatesX,
         TobiiProFusionChannel.RightGazeOriginInTrackBoxCoordinatesY,
         TobiiProFusionChannel.RightGazeOriginInTrackBoxCoordinatesZ]]

    right_gaze_origin_valid = gaze_data_t[TobiiProFusionChannel.RightGazeOriginValid]
    right_gaze_point_valid = gaze_data_t[TobiiProFusionChannel.RightGazePointValid]

    right_pupil_diameter = gaze_data_t[TobiiProFusionChannel.RightPupilDiameter]
    right_pupil_diameter_valid = gaze_data_t[TobiiProFusionChannel.RightPupilDiameterValid]

    right_gaze_point_on_display_area = gaze_data_t[
        [TobiiProFusionChannel.RightGazePointOnDisplayAreaX, TobiiProFusionChannel.RightGazePointOnDisplayAreaY]]

    right_eye_gaze_data = EyeData(gaze_origin_in_user_coordinate=right_gaze_origin_in_user_coordinate,
                                  gaze_point_in_user_coordinate=right_gaze_point_in_user_coordinate,
                                  gaze_origin_valid=right_gaze_origin_valid,
                                  gaze_point_valid=right_gaze_point_valid,
                                  gaze_origin_in_trackbox_coordinate=right_gaze_origin_in_track_box_coordinate,
                                  pupil_diameter=right_pupil_diameter,
                                  pupil_diameter_valid=right_pupil_diameter_valid,
                                  gaze_point_on_display_area=right_gaze_point_on_display_area,
                                  timestamp=timestamp)

    gaze_data_ta = GazeData(left_eye_gaze_data=left_eye_gaze_data, right_eye_gaze_data = right_eye_gaze_data)
    # print('Processed')
    pass

