# import enum

import scipy.signal

import pandas

# class FilterTypes(enum.Enum):

#     lowpass = 1
#     higpass = 2
#     bandpass = 3
#     highpass = 4


class BaseFilter:

    def __call__(self, input):

        return scipy.signal.filtfilt(
            self.b, self.a, input, axis=0
        )
    
    def window(self, filter_type):
        return scipy.signal.butter(
            self.order, self.Wn, filter_type, analog=False
        )


class BandStop(BaseFilter):

    def __init__(self, hz, sampling, band=(3,3)):
        
        self.hz = hz
        self.band = band

        self.sampling = sampling
        self.nyquist = self.sampling // 2
        
        self.order = 2
        self.Wn = (self.hz-self.band[0])/self.nyquist, (self.hz+self.band[0])/self.nyquist

        self.b, self.a = self.window('bandstop')



class LowPass(BaseFilter):

    def __init__(self, hz, sampling):
        
        self.hz = hz

        self.sampling = sampling
        self.nyquist = self.sampling // 2
        
        self.order = 3
        self.Wn = self.hz / self.nyquist

        self.b, self.a = self.window('lowpass')
