import pickle
import matplotlib.pyplot as plt

from examples.TobiiEyeTrackerConfig import TobiiProFusionChannel

file_path = 'TobiiGazeData.pickle'
# Open the file in binary mode
with open(file_path, 'rb') as file:
    # Load the data from the file
    gaze_raw = pickle.load(file)

gaze_data = gaze_raw['TobiiProFusionUnityLSLOutlet'][0]


# invalid label




left_eye_gaze_origin_valid = gaze_data[TobiiProFusionChannel.LeftGazeOriginValid.value]
left_eye_gaze_point_valid = gaze_data[TobiiProFusionChannel.LeftGazePointValid.value]
left_eye_pupil_diameter_valid = gaze_data[TobiiProFusionChannel.LeftPupilDiameterValid.value]


right_eye_gaze_origin_valid = gaze_data[TobiiProFusionChannel.RightGazeOriginValid.value]
right_eye_gaze_point_valid = gaze_data[TobiiProFusionChannel.RightGazePointValid.value]
right_eye_pupil_diameter_valid = gaze_data[TobiiProFusionChannel.RightPupilDiameterValid.value]


left_eye_on_display_area_x = gaze_data[TobiiProFusionChannel.LeftGazePointOnDisplayAreaX.value]
left_eye_on_display_area_y = gaze_data[TobiiProFusionChannel.LeftGazePointOnDisplayAreaY.value]

plt.plot(left_eye_on_display_area_x[0:1500], left_eye_on_display_area_y[0:1500])
plt.xlim(0,1)
plt.ylim(0,1)
plt.show()

#
# right_eye_gaze_point_valid = gaze_data[TobiiProFusionChannel.RightGazePointValid.value]
# right_eye_on_display_area_x = gaze_data[TobiiProFusionChannel.RightGazePointOnDisplayAreaX.value]
# right_eye_on_display_area_y = gaze_data[TobiiProFusionChannel.RightGazePointOnDisplayAreaY.value]








