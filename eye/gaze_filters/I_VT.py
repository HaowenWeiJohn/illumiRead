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



