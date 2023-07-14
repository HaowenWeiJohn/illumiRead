import numpy as np

class illumiReadError(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)
    """Base class for other exceptions"""
    pass



class DataProcessorEvokeFailedError(illumiReadError):
    def __init__(self, error):
        super().__init__(error)
        self.error = error

    def __str__(self):
        return 'DataProcessorEvokeFailedError: ' + self.error



class DaProcessorNotchFilterInvalidQError(DataProcessorEvokeFailedError):
    def __init__(self, error):
        super().__init__(error)
        self.error = error

    def __str__(self):
        return self.error #+ 'DaProcessorNotchFilterInvalidQError'

class DataProcessorInvalidFrequencyError(DataProcessorEvokeFailedError):
    def __init__(self, error):
        super().__init__(error)
        self.error = error

    def __str__(self):
        return self.error #+ 'DataProcessorInvalidFrequencyError'

class DataProcessorInvalidBufferSizeError(DataProcessorEvokeFailedError):
    def __init__(self, error):
        super().__init__(error)
        self.error = error

    def __str__(self):
        return self.error #+ 'DataProcessorInvalidBufferSizeError'


