# channel_info = [
#     "CombinedGazeRayScreenDirectionX",
#     "CombinedGazeRayScreenDirectionY",
#     "CombinedGazeRayScreenDirectionZ",
#     "CombinedGazeRayScreenOriginX",
#     "CombinedGazeRayScreenOriginY",
#     "CombinedGazeRayScreenOriginZ",
#     "CombinedGazeRayScreenOriginValid",
#     "LeftGazeOriginInTrackBoxCoordinatesX",
#     "LeftGazeOriginInTrackBoxCoordinatesY",
#     "LeftGazeOriginInTrackBoxCoordinatesZ",
#     "LeftGazeOriginInUserCoordinatesX",
#     "LeftGazeOriginInUserCoordinatesY",
#     "LeftGazeOriginInUserCoordinatesZ",
#     "LeftGazeOriginValid",
#     "LeftGazePointInUserCoordinatesX",
#     "LeftGazePointInUserCoordinatesY",
#     "LeftGazePointInUserCoordinatesZ",
#     "LeftGazePointOnDisplayAreaX",
#     "LeftGazePointOnDisplayAreaY",
#     "LeftGazePointValid",
#     "LeftGazeRayScreenDirectionX",
#     "LeftGazeRayScreenDirectionY",
#     "LeftGazeRayScreenDirectionZ",
#     "LeftGazeRayScreenOriginX",
#     "LeftGazeRayScreenOriginY",
#     "LeftGazeRayScreenOriginZ",
#     "LeftPupileDiameter",
#     "LeftPupileDiameterValid",
#     "RightGazeOriginInTrackBoxCoordinatesX",
#     "RightGazeOriginInTrackBoxCoordinatesY",
#     "RightGazeOriginInTrackBoxCoordinatesZ",
#     "RightGazeOriginInUserCoordinatesX",
#     "RightGazeOriginInUserCoordinatesY",
#     "RightGazeOriginInUserCoordinatesZ",
#     "RightGazeOriginValid",
#     "RightGazePointInUserCoordinatesX",
#     "RightGazePointInUserCoordinatesY",
#     "RightGazePointInUserCoordinatesZ",
#     "RightGazePointOnDisplayAreaX",
#     "RightGazePointOnDisplayAreaY",
#     "RightGazePointValid",
#     "RightGazeRayScreenDirectionX",
#     "RightGazeRayScreenDirectionY",
#     "RightGazeRayScreenDirectionZ",
#     "RightGazeRayScreenOriginX",
#     "RightGazeRayScreenOriginY",
#     "RightGazeRayScreenOriginZ",
#     "RightPupilDiameter",
#     "RightPupilDiameterValid",
#     "OriginalGazeDeviceTimeStamp",
#     "OriginalGazeSystemTimeStamp"
# ]
# import enum

from enum import Enum

class TobiiProFusionChannel(Enum):
    CombinedGazeRayScreenDirectionX = 0
    CombinedGazeRayScreenDirectionY = 1
    CombinedGazeRayScreenDirectionZ = 2
    CombinedGazeRayScreenOriginX = 3
    CombinedGazeRayScreenOriginY = 4
    CombinedGazeRayScreenOriginZ = 5
    CombinedGazeRayScreenOriginValid = 6
    LeftGazeOriginInTrackBoxCoordinatesX = 7
    LeftGazeOriginInTrackBoxCoordinatesY = 8
    LeftGazeOriginInTrackBoxCoordinatesZ = 9
    LeftGazeOriginInUserCoordinatesX = 10
    LeftGazeOriginInUserCoordinatesY = 11
    LeftGazeOriginInUserCoordinatesZ = 12
    LeftGazeOriginValid = 13
    LeftGazePointInUserCoordinatesX = 14
    LeftGazePointInUserCoordinatesY = 15
    LeftGazePointInUserCoordinatesZ = 16
    LeftGazePointOnDisplayAreaX = 17
    LeftGazePointOnDisplayAreaY = 18
    LeftGazePointValid = 19
    LeftGazeRayScreenDirectionX = 20
    LeftGazeRayScreenDirectionY = 21
    LeftGazeRayScreenDirectionZ = 22
    LeftGazeRayScreenOriginX = 23
    LeftGazeRayScreenOriginY = 24
    LeftGazeRayScreenOriginZ = 25
    LeftPupilDiameter = 26
    LeftPupilDiameterValid = 27
    RightGazeOriginInTrackBoxCoordinatesX = 28
    RightGazeOriginInTrackBoxCoordinatesY = 29
    RightGazeOriginInTrackBoxCoordinatesZ = 30
    RightGazeOriginInUserCoordinatesX = 31
    RightGazeOriginInUserCoordinatesY = 32
    RightGazeOriginInUserCoordinatesZ = 33
    RightGazeOriginValid = 34
    RightGazePointInUserCoordinatesX = 35
    RightGazePointInUserCoordinatesY = 36
    RightGazePointInUserCoordinatesZ = 37
    RightGazePointOnDisplayAreaX = 38
    RightGazePointOnDisplayAreaY = 39
    RightGazePointValid = 40
    RightGazeRayScreenDirectionX = 41
    RightGazeRayScreenDirectionY = 42
    RightGazeRayScreenDirectionZ = 43
    RightGazeRayScreenOriginX = 44
    RightGazeRayScreenOriginY = 45
    RightGazeRayScreenOriginZ = 46
    RightPupilDiameter = 47
    RightPupilDiameterValid = 48
    OriginalGazeDeviceTimeStamp = 49
    OriginalGazeSystemTimeStamp = 50