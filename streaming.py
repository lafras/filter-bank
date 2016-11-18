import numpy
from numpy import linspace
from numpy import pi, sin

import scipy.signal
import scipy.stats

import pandas

import statsmodels.api as sm

import rx

import filters
import noisy_signal


class Reporter(rx.Observer):

    def on_next(self, frame: pandas.DataFrame):
        print(
            frame.head()
        )
    # def on_next(self, x):
    #     print(
    #         x
    #     )

    def on_error(self, e):
        print(
            e
        )

    def on_completed(self):
        pass


class FilterBank:

    def __init__(self, stop, steps):

        self.stop = stop
        self.steps = steps

        self.remove_hz=1/7
        self.sampling_hz = (steps-1) / stop
        self.hz_band=(1/14, 6/7)


    def run(self):

        bandstop = filters.BandStop(
            self.remove_hz, self.sampling_hz, self.hz_band
        )

        self.observable = rx.Observable

        self.observable = self.observable.range(
            10, 5
        ).map(
            self.signal
        ).map(
            self.filter
        )

        reporter = Reporter()
        self.observable.subscribe(
            # print
            reporter
        )
        
    def signal(self, x, idx):
        return noisy_signal.noisy_signal(self.stop, self.steps)

    def filter(self, frame, idx):

        bandstop = filters.BandStop(
            self.remove_hz, self.sampling_hz, self.hz_band
        )
        frame['seasonless'] = bandstop(frame['signal'].values)
        
        return frame



if __name__ == '__main__':
    
    f = FilterBank(
        1.0, 20
    )
    f.run()
