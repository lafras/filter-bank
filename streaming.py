"""Combine scipy filters, RxPy and pyfilesystems"""

import numpy
from numpy import linspace
from numpy import pi, sin

import scipy.signal
import scipy.stats

import pandas

import statsmodels.api as sm

import fs.osfs
import rx

import filters
import noisy_signal


class Reporter(rx.Observer):

    def on_next(self, frame):
        print(
            frame.head()
        )

    def on_error(self, e):
        print(
            'Stream broke with error: {}'.format(e)
        )

    def on_completed(self):
        pass


class FilterBank:

    def __init__(self):
        self.root = fs.osfs.OSFS('./')
        

    def run(self, stop, steps):

        self.remove_hz=1/7
        self.sampling_hz = (steps-1) / stop
        self.hz_band=(1/14, 6/7)

        self.stop = stop
        self.steps = steps

        bandstop = filters.BandStop(
            self.remove_hz, self.sampling_hz, self.hz_band
        )

        self.observable = rx.Observable

        self.observable = self.observable.range(
            1, 5
        ).map(
            self.signal
        ).map(
            self.filter
        ).map(
            self.save
        )

        reporter = Reporter()
        self.observable.subscribe(
            reporter
        )
        
    def signal(self, idx):
        frame = noisy_signal.noisy_signal(
            self.stop, self.steps
        )
        return frame

    def filter(self, frame, idx):
        bandstop = filters.BandStop(
            self.remove_hz, self.sampling_hz, self.hz_band
        )
        frame['seasonless'] = bandstop(
            frame['signal'].values
        )
        return frame

    def save(self, frame, idx):
        seasonless = self.root.makeopendir('seasonless')
        frame.to_csv(
            seasonless.open(
                '{}.csv'.format(idx+1),
                mode='w'
            )
        )
        return frame


if __name__ == '__main__':
    
    f = FilterBank()
    f.run(
        1.0, 20
    )
