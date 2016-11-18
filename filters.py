import scipy.signal

import pandas

class BaseFilter:

    def __call__(self, input):

        return scipy.signal.filtfilt(
            self.b, self.a, input, axis=0
        )
    

class BandStop(BaseFilter):

    def __init__(self, hz, sampling, band=(3,3)):
        
        self.hz = hz
        self.band = band

        self.sampling = sampling
        self.nyquist = self.sampling // 2
        
        self.order = 2
        self.Wn = (self.hz-self.band[0])/self.nyquist, (self.hz+self.band[0])/self.nyquist

        self.b, self.a = self.window()

    def window(self):
        return scipy.signal.butter(self.order, self.Wn, 'bandstop', analog=False)


class LowPass(BaseFilter):

    def __init__(self, hz, sampling):
        
        self.hz = hz
        # self.threshold = threshold

        self.sampling = sampling
        self.nyquist = self.sampling // 2
        
        self.order = 3
        self.Wn = self.hz / self.nyquist #(self.hz-self.band[0])/self.nyquist, (self.hz+self.band[0])/self.nyquist

        self.b, self.a = self.window()

    def window(self):
        return scipy.signal.butter(self.order, self.Wn, 'lowpass', analog=False)

