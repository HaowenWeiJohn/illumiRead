import numpy as np

from utils.DataProcessors import DataProcessor, DataProcessorType



# gap fill-in 75ms

# eye selection average

# noise reduction: disabled

# velocity calculator: window length 20ms

# velocity threshold: 30 deg/s



class RealtimeFxiationDetectionIVT(DataProcessor):

    def __init__(self):
        super().__init__(data_processor_type=DataProcessorType.CustomDataProcessor)



class RealtimeFxiationDetectionIDT(DataProcessor):

    def __init__(self, sampling_frequency, time_unit_scale_factor, max_gap_length, angular_velocity_degree_limit):
        super().__init__(data_processor_type=DataProcessorType.CustomDataProcessor)
