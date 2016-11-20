import glob
import os
import unittest
import numpy
import pandas
import luigi


class BatchingTestCase(unittest.TestCase):
    
    def setUp(self):
    
        import batching

        self.uid = 1

        for csv in glob.glob('*/{}.csv'.format(self.uid)):
            print(csv)
            os.remove(csv)

        self.filter_bank = batching.FilterBank(self.uid)
        
        luigi.build([self.filter_bank], local_scheduler=True)


    def test_allclose(self):
        
        noise = pandas.read_csv(
            'noise/{}.csv'.format(self.uid),
            index_col=0
        )
        
        seasonless = pandas.read_csv(
            'seasonless/{}.csv'.format(self.uid),
            index_col=0
        )

        self.assertTrue(
            numpy.allclose(
                noise[['trend', 'cycle']].sum(axis=1), 
                seasonless['seasonless'],
                rtol=0.5
            )
        )

    def tearDown(self):
        
        for csv in glob.glob('*/{}.csv'.format(self.uid)):
            os.remove(csv)


class StreamingTestCase(unittest.TestCase):
    
    def setUp(self):
    
        import streaming

        self.filter_bank = streaming.FilterBank()
        

    def test_allclose(self):
        
        self.filter_bank.run(1.0, 20)
        seasonless = self.filter_bank.root.opendir('seasonless')

        for csv in seasonless.listdir():
            s = pandas.read_csv(
                seasonless.open(
                    csv,
                    mode='r'
                ),
                index_col=0
            )
            self.assertTrue(
                numpy.allclose(
                    s['signal'], 
                    s['seasonless'],
                    rtol=0.5
                )
            )

    def tearDown(self):
        self.filter_bank.root.removedir(
            'seasonless', force=True
        )
        