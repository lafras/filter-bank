import numpy
from numpy import linspace
from numpy import pi, sin

import scipy.signal
import scipy.stats

import pandas


def noisy_signal(stop, steps):

    ts, dt = linspace(0.0, stop, steps, retstep=True)
    
    a, b = 2, 1/7

    frame = pandas.DataFrame(
        data={
            'trend':  5.0,
            'cycle':  0.5 * sin(2*pi*a*ts),
            'season': 1 * sin(2*pi*b*ts),
            'noise':  scipy.stats.norm.rvs(0, 0.3)
        },
        index=ts
    )
    frame['signal'] = frame.sum(axis=1)

    return frame