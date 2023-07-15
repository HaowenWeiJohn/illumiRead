import enum

import numpy as np


class GazeType(enum.Enum):
    Saccade = 1
    Fixation = 2
    Unknown = 0

class EyeData:
    def __init__(self, gaze_origin_in_user_coordinate=np.array([0, 0, 0]),
                 gaze_point_in_user_coordinate=np.array([0, 0, 0]), gaze_origin_valid=False,
                 gaze_point_valid=False,
                 gaze_origin_in_trackbox_coordinate=np.array([0, 0, 0]),
                 pupil_diameter=0.0,
                 pupil_diameter_valid=False,
                 timestamp=0):

        self.gaze_origin_in_user_coordinate = gaze_origin_in_user_coordinate
        self.gaze_point_in_user_coordinate = gaze_point_in_user_coordinate
        self.gaze_origin_valid = gaze_origin_valid
        self.gaze_point_valid = gaze_point_valid
        self.gaze_origin_in_trackbox_coordinate = gaze_origin_in_trackbox_coordinate
        self.pupil_diameter = pupil_diameter
        self.pupil_diameter_valid = pupil_diameter_valid
        self.timestamp = timestamp

        self.gaze_direction = np.array([0, 0, 0])
        if gaze_origin_valid:
            self.gaze_direction = self.get_gaze_direction()

    def get_gaze_direction(self, normalize=True):
        gaze_direction = self.gaze_point_in_user_coordinate - self.gaze_origin_in_user_coordinate
        if normalize:
            gaze_direction = gaze_direction / np.linalg.norm(gaze_direction)
        return gaze_direction


class GazeData:

    def __init__(self, left_eye_data: EyeData, right_eye_data: EyeData):
        self.left_eye_data = left_eye_data
        self.right_eye_data = right_eye_data
        self.combined_eye_data = self.get_combined_eye_data()
        self.timestamp = self.combined_eye_data.timestamp

        self.gaze_type = GazeType.Unknown

    def get_combined_eye_data(self):
        return EyeData(
            gaze_origin_in_user_coordinate=(self.left_eye_data.gaze_origin_in_user_coordinate + self.right_eye_data.gaze_origin_in_user_coordinate) / 2,
            gaze_point_in_user_coordinate=(self.left_eye_data.gaze_point_in_user_coordinate + self.right_eye_data.gaze_point_in_user_coordinate) / 2,
            gaze_origin_valid=self.left_eye_data.gaze_origin_valid and self.right_eye_data.gaze_origin_valid,
            gaze_point_valid=self.left_eye_data.gaze_point_valid and self.right_eye_data.gaze_point_valid,
            gaze_origin_in_trackbox_coordinate=(self.left_eye_data.gaze_origin_in_trackbox_coordinate + self.right_eye_data.gaze_origin_in_trackbox_coordinate) / 2,
            pupil_diameter=(self.left_eye_data.pupil_diameter + self.right_eye_data.pupil_diameter) / 2,
            pupil_diameter_valid=self.left_eye_data.pupil_diameter_valid and self.right_eye_data.pupil_diameter_valid,
            timestamp=self.left_eye_data.timestamp
        )
