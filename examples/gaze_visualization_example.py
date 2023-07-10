from rena.utils.data_utils import RNStream

file_path = 'D:/HaowenWei/Data'
gaze_data = RNStream(file_path = file_path)
data = gaze_data.stream_in(jitter_removal=False)
