import pickle
import matplotlib.pyplot as plt
import numpy as np
from examples.TobiiEyeTrackerConfig import TobiiProFusionChannel
from utils.general_utils import angle_between_vectors, angular_velocity_between_vectors_radians, \
    angular_velocity_between_vectors_degrees, init_fifo_buffer, calculate_angular_dispersion

file_path = 'TobiiGazeData.pickle'
# Open the file in binary mode
with open(file_path, 'rb') as file:
    # Load the data from the file
    gaze_raw = pickle.load(file)

gaze_data = gaze_raw['TobiiProFusionUnityLSLOutlet'][0]
timestamps = gaze_raw['TobiiProFusionUnityLSLOutlet'][1]

# invalid label


left_eye_gaze_origin_valid = gaze_data[TobiiProFusionChannel.LeftGazeOriginValid]
left_eye_gaze_point_valid = gaze_data[TobiiProFusionChannel.LeftGazePointValid]
left_eye_pupil_diameter_valid = gaze_data[TobiiProFusionChannel.LeftPupilDiameterValid]

right_eye_gaze_origin_valid = gaze_data[TobiiProFusionChannel.RightGazeOriginValid]
right_eye_gaze_point_valid = gaze_data[TobiiProFusionChannel.RightGazePointValid]
right_eye_pupil_diameter_valid = gaze_data[TobiiProFusionChannel.RightPupilDiameterValid]

left_eye_on_display_area_x = gaze_data[TobiiProFusionChannel.LeftGazePointOnDisplayAreaX]
left_eye_on_display_area_y = gaze_data[TobiiProFusionChannel.LeftGazePointOnDisplayAreaY]

plt.plot(left_eye_on_display_area_x[0:1500], left_eye_on_display_area_y[0:1500])
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()

# gap filling
# test IDT example


sampling_frequency = 250
# while there are still point
sampling_frequency_duration_unit_scaling_factor = 1000  # millisecond
max_gap_length = 75  # millisecond
gap_fill_check_buffer_size = sampling_frequency*(max_gap_length/sampling_frequency_duration_unit_scaling_factor)  # 75 ms
angular_velocity_limit_degree = 1000  # degree per second

buffer_duration = 150  # millisecond
gaze_vector_buffer = init_fifo_buffer(duration=buffer_duration, sampling_frequency=sampling_frequency, channel_number=3, sampling_frequency_duration_unit_scaling_factor=1000,
                       fill_value=0, dtype=np.float64)

last_timestamp = 0
last_combined_gaze_vector_normalized = np.array([0, 0, 1])




for index, timestamp in enumerate(timestamps):
    gaze_data_t = gaze_data[:, index]
    left_eye_gaze_point_valid = gaze_data_t[TobiiProFusionChannel.LeftGazePointValid]
    right_eye_gaze_point_valid = gaze_data_t[TobiiProFusionChannel.RightGazePointValid]

    left_eye_gaze_origin = gaze_data_t[[TobiiProFusionChannel.LeftGazeOriginInUserCoordinatesX,
                                        TobiiProFusionChannel.LeftGazeOriginInUserCoordinatesY,
                                        TobiiProFusionChannel.LeftGazeOriginInUserCoordinatesZ]]

    left_eye_gaze_point = gaze_data_t[[TobiiProFusionChannel.LeftGazePointInUserCoordinatesX,
                                       TobiiProFusionChannel.LeftGazePointInUserCoordinatesY,
                                       TobiiProFusionChannel.LeftGazePointInUserCoordinatesZ]]

    right_eye_gaze_origin = gaze_data_t[[TobiiProFusionChannel.RightGazeOriginInUserCoordinatesX,
                                         TobiiProFusionChannel.RightGazeOriginInUserCoordinatesY,
                                         TobiiProFusionChannel.RightGazeOriginInUserCoordinatesZ]]

    right_eye_gaze_point = gaze_data_t[[TobiiProFusionChannel.RightGazePointInUserCoordinatesX,
                                        TobiiProFusionChannel.RightGazePointInUserCoordinatesY,
                                        TobiiProFusionChannel.RightGazePointInUserCoordinatesZ]]

    left_gaze_vector = left_eye_gaze_point - left_eye_gaze_origin
    right_gaze_vector = right_eye_gaze_point - right_eye_gaze_origin

    left_gaze_vector_normalized = left_gaze_vector / np.linalg.norm(left_gaze_vector)
    right_gaze_vector_normalized = right_gaze_vector / np.linalg.norm(right_gaze_vector)

    # combine left and right gaze vector to get the combined gaze vector
    combined_gaze_vector = left_gaze_vector_normalized + right_gaze_vector_normalized
    combined_gaze_vector_normalized = combined_gaze_vector / np.linalg.norm(combined_gaze_vector) ## add to buffer

    gaze_vector_buffer.push(combined_gaze_vector_normalized)
    if gaze_vector_buffer.is_full():
        dispersion = calculate_angular_dispersion(gaze_vector_buffer.buffer)

    angular_velocity = angular_velocity_between_vectors_degrees(last_combined_gaze_vector_normalized,
                                                                combined_gaze_vector_normalized,
                                                                sampling_frequency)




    gaze_vector_buffer.push(combined_gaze_vector_normalized)









    # if angular velocity is too large, skip




    # calculate angular velocity between two gaze vectors



    # print(combined_gaze_vector_normalized)
    #
    #
    # # fixation detection algorithm
    # # I-DT
    # # 1. if the current point is invalid, skip
    #

    pass

#
# right_eye_gaze_point_valid = gaze_data[TobiiProFusionChannel.RightGazePointValid.value]
# right_eye_on_display_area_x = gaze_data[TobiiProFusionChannel.RightGazePointOnDisplayAreaX.value]
# right_eye_on_display_area_y = gaze_data[TobiiProFusionChannel.RightGazePointOnDisplayAreaY.value]
