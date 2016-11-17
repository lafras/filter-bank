import pandas
from matplotlib.pyplot import show


class Plot:

    def __init__(self, uid):

        self.uid = uid

        self.noise = pandas.read_csv(
            'noise/{}.csv'.format(self.uid),
            index_col=0
        )
        self.noise['test'] = self.noise[['trend', 'cycle']].sum(axis=1)
        self.seasonless = pandas.read_csv(
            'seasonless/{}.csv'.format(self.uid),
            index_col=0
        )

    def plot(self):

        self.noise.plot()
        self.seasonless.plot()

        show()

if __name__ == '__main__':
    
    p = Plot(1)
    p.plot()