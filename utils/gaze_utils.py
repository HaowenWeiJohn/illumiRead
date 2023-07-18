import enum

import numpy as np


class GazeType(enum.Enum):
    SACCADE = 1
    FIXATION = 2
    UNDETERMINED = 0

class EyeData:
    def __init__(self, gaze_origin_in_user_coordinate=np.array([0, 0, 0]),
                 gaze_point_in_user_coordinate=np.array([0, 0, 0]), gaze_origin_valid=False,
                 gaze_point_valid=False,
                 gaze_origin_in_trackbox_coordinate=np.array([0, 0, 0]),
                 pupil_diameter=0.0,
                 pupil_diameter_valid=False,
                 gaze_point_on_display_area = np.array([0, 0]),
                 timestamp=0):

        self.gaze_origin_in_user_coordinate = gaze_origin_in_user_coordinate
        self.gaze_point_in_user_coordinate = gaze_point_in_user_coordinate
        self.gaze_origin_valid = gaze_origin_valid
        self.gaze_point_valid = gaze_point_valid
        self.gaze_origin_in_trackbox_coordinate = gaze_origin_in_trackbox_coordinate
        self.pupil_diameter = pupil_diameter
        self.pupil_diameter_valid = pupil_diameter_valid
        self.gaze_point_on_display_area = gaze_point_on_display_area
        self.timestamp = timestamp

        self.gaze_direction = np.array([0, 0, 0])

        if self.gaze_origin_valid and self.gaze_point_valid:
            self.gaze_direction = self.get_gaze_direction()

    def get_gaze_direction(self, normalize=True):
        gaze_direction = self.gaze_point_in_user_coordinate - self.gaze_origin_in_user_coordinate
        if normalize:
            gaze_direction = gaze_direction / np.linalg.norm(gaze_direction)
        return gaze_direction


class GazeData:

    def __init__(self, left_eye_gaze_data: EyeData, right_eye_gaze_data: EyeData):
        self.left_eye_gaze_data = left_eye_gaze_data
        self.right_eye_gaze_data = right_eye_gaze_data
        self.combined_eye_gaze_data = self.get_combined_eye_gaze_data()
        self.timestamp = self.combined_eye_gaze_data.timestamp

        self.gaze_type = GazeType.UNDETERMINED

    def get_combined_eye_gaze_data(self):
        return EyeData(
            gaze_origin_in_user_coordinate=(self.left_eye_gaze_data.gaze_origin_in_user_coordinate + self.right_eye_gaze_data.gaze_origin_in_user_coordinate) / 2,
            gaze_point_in_user_coordinate=(self.left_eye_gaze_data.gaze_point_in_user_coordinate + self.right_eye_gaze_data.gaze_point_in_user_coordinate) / 2,
            gaze_origin_valid=self.left_eye_gaze_data.gaze_origin_valid and self.right_eye_gaze_data.gaze_origin_valid,
            gaze_point_valid=self.left_eye_gaze_data.gaze_point_valid and self.right_eye_gaze_data.gaze_point_valid,
            gaze_origin_in_trackbox_coordinate=(self.left_eye_gaze_data.gaze_origin_in_trackbox_coordinate + self.right_eye_gaze_data.gaze_origin_in_trackbox_coordinate) / 2,
            pupil_diameter=(self.left_eye_gaze_data.pupil_diameter + self.right_eye_gaze_data.pupil_diameter) / 2,
            pupil_diameter_valid=self.left_eye_gaze_data.pupil_diameter_valid and self.right_eye_gaze_data.pupil_diameter_valid,
            gaze_point_on_display_area= (self.left_eye_gaze_data.gaze_point_on_display_area + self.right_eye_gaze_data.gaze_point_on_display_area) / 2,
            timestamp=self.left_eye_gaze_data.timestamp
        )
