from utils.DataProcessors import *

class GazeFilterIDT(DataProcessor):
    def __init__(self):
        super().__init__(duration=0.1, sampling_frequency=100, channel_number=2)
        pass
        # self.filter = IDTFilter()
        # self.filter.set_calibration_data(0.5, 0.5, 0.5, 0.5, 0.5, 0.5)