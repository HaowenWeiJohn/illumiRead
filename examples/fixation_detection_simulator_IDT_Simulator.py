import pickle
import matplotlib.pyplot as plt
import numpy as np
from examples.TobiiEyeTrackerConfig import TobiiProFusionChannel
from utils.GazeFilter import GazeDataGapFilling, GazeFilterFixationDetectionIDTAngular
from utils.gaze_utils import EyeData, GazeData, GazeType
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


sampling_frequency = 250.0
# while there are still point
sampling_frequency_unit_duration_unit_scaling_factor = 1000  # millisecond
max_gap_duration = 75  # millisecond
# gap_fill_check_buffer_size = sampling_frequency * (
#             max_gap_duration / sampling_frequency_unit_duration_unit_scaling_factor)  # 75 ms
angular_velocity_limit_degree = 1000  # degree per second

buffer_duration = 150  # millisecond

idt_filter = GazeFilterFixationDetectionIDTAngular(sampling_frequency=250, duration=150,
                                                   sampling_frequency_unit_duration_unit_scaling_factor=1000,
                                                   angular_threshold_degree=1.5, dtype=np.float64)
idt_filter.evoke_data_processor()
gaze_data_classified = []

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

    Gaze_Data_T = GazeData(left_eye_gaze_data=left_eye_gaze_data, right_eye_gaze_data=right_eye_gaze_data)
    Gaze_Data_T_classified = idt_filter.process_sample(Gaze_Data_T)
    gaze_data_classified.append(Gaze_Data_T_classified)

print("done")
plt.xlim(0, 1)
plt.ylim(0, 1)
for index, gaze_data in enumerate(gaze_data_classified):

    if gaze_data.gaze_type == GazeType.FIXATION:
        color = 'red'
        plt.scatter(gaze_data.combined_eye_gaze_data.gaze_point_on_display_area[0],
                    gaze_data.combined_eye_gaze_data.gaze_point_on_display_area[1], color=color)


    elif gaze_data.gaze_type == GazeType.SACCADE:
        color = 'blue'
        plt.scatter(gaze_data.combined_eye_gaze_data.gaze_point_on_display_area[0],
                    gaze_data.combined_eye_gaze_data.gaze_point_on_display_area[1], color=color)

    if index==1500:
        pass
