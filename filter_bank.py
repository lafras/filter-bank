import numpy
from numpy import linspace
from numpy import pi, sin

import scipy.signal
import scipy.stats

import pandas

import statsmodels.api as sm

import luigi


def signal():
    

    return ts, (trend + cycle + season + noise), 1/dt


class NoisySignal(luigi.Task):
    
    uid = luigi.IntParameter()
    stop = luigi.FloatParameter(
        default=10*pi
    )
    steps = luigi.IntParameter(
        default=10**4
    )

    def requires(self):
        return None

    def output(self):
        return luigi.LocalTarget(
            'noise/{}.csv'.format(self.uid)
        )
    def run(self):

        ts, dt = linspace(0.0, self.stop, self.steps, retstep=True)
        
        # a, b, c = 10, 1/7, 1/31
        a, b = 2, 1/7

        frame = pandas.DataFrame(
            data={
                'trend':  5.0,
                'cycle':  0.5 * sin(2*pi*a*ts),
                'season': 1 * sin(2*pi*b*ts),
                # 'noise':  scipy.stats.norm.rvs(0, 0.3)
            },
            index=ts
        )
        frame['signal'] = frame.sum(axis=1)


        with self.output().open('w') as output:
            frame.to_csv(
                output
            )

class RemoveSeasons(luigi.Task):

    uid = luigi.IntParameter()
    upstream_task = luigi.Parameter()
    remove_hz = luigi.FloatParameter()
    sampling_hz = luigi.FloatParameter()
    hz_band = luigi.Parameter()

    def requires(self):
        return self.upstream_task

    def output(self):
        return luigi.LocalTarget(
            'seasonless/{}.csv'.format(self.uid)
        )

    def run(self):
        with self.input().open('r') as input:
            frame = pandas.read_csv(
                input, index_col=0
            )

        order = 2
        nyquist = self.sampling_hz / 2
        window = (self.remove_hz - self.hz_band[0]) / nyquist, (self.remove_hz + self.hz_band[1]) / nyquist

        right, left = scipy.signal.butter(order, window, 'bandstop')

        frame['seasonless'] = scipy.signal.filtfilt(
            right, left, frame['signal'].values
        )

        with self.output().open('w') as output:
            frame.to_csv(
                output
            )

class FilterBank(luigi.Task):

    uid = luigi.IntParameter()

    def requires(self):
        
        stop = 4.5*pi
        steps = 10**3

        signal = NoisySignal(
            uid=self.uid,
            stop=stop,
            steps=steps
        )
        cleaned = RemoveSeasons(
            uid=self.uid,
            upstream_task=signal,
            remove_hz=1/7,
            sampling_hz = (steps-1) / stop,
            hz_band=(1/14, 1/14)
        )
        return cleaned

    def output(self):
        return self.input()


if __name__ == '__main__':
    
    uid = 1

    luigi.build([FilterBank(uid)], local_scheduler=True)
    # luigi.run(['--local-scheduler', '--no-lock', 'FilterBank', '--uid', '3'])

    import pltr

    p = pltr.Plot(uid)
    p.plot()


