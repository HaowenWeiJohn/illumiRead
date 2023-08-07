import enum

import numpy as np

from examples.TobiiEyeTrackerConfig import TobiiProFusionChannel


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

    def __init__(self, left_eye_gaze_data: EyeData = EyeData(), right_eye_gaze_data: EyeData = EyeData()):
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

    def construct_gaze_data_tobii_pro_fusion(self, gaze_data_t):

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

        self.left_eye_gaze_data = EyeData(
            gaze_origin_in_user_coordinate=left_gaze_origin_in_user_coordinate,
            gaze_point_in_user_coordinate=left_gaze_point_in_user_coordinate,
            gaze_origin_valid=left_gaze_origin_valid,
            gaze_point_valid=left_gaze_point_valid,
            gaze_origin_in_trackbox_coordinate=left_gaze_origin_in_track_box_coordinate,
            pupil_diameter=left_pupil_diameter,
            pupil_diameter_valid=left_pupil_diameter_valid,
            gaze_point_on_display_area=left_gaze_point_on_display_area,
            timestamp=gaze_data_t[TobiiProFusionChannel.OriginalGazeDeviceTimeStamp])

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

        self.right_eye_gaze_data = EyeData(
            gaze_origin_in_user_coordinate=right_gaze_origin_in_user_coordinate,
            gaze_point_in_user_coordinate=right_gaze_point_in_user_coordinate,
            gaze_origin_valid=right_gaze_origin_valid,
            gaze_point_valid=right_gaze_point_valid,
            gaze_origin_in_trackbox_coordinate=right_gaze_origin_in_track_box_coordinate,
            pupil_diameter=right_pupil_diameter,
            pupil_diameter_valid=right_pupil_diameter_valid,
            gaze_point_on_display_area=right_gaze_point_on_display_area,
            timestamp=TobiiProFusionChannel.OriginalGazeDeviceTimeStamp)

        self.get_combined_eye_gaze_data()

