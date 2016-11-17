import unittest
import numpy
import pandas
import luigi


class MultiplicationRuleTestCase(unittest.TestCase):
    
    def setUp(self):
    
        import filter_bank

        self.uid = 1
        self.filter_bank = filter_bank.FilterBank(self.uid)
        

    def test_filter_bank(self):
        
        luigi.build([self.filter_bank], local_scheduler=True)
        
        noise = pandas.read_csv(
            'noise/{}.csv'.format(self.uid),
            index_col=0
        )
        print(noise.head())
        seasonless = pandas.read_csv(
            'seasonless/{}.csv'.format(self.uid),
            index_col=0
        )

        self.assertTrue(
            numpy.allclose(
                noise[['trend', 'cycle']].sum(axis=1), 
                seasonless['seasonless']
            )
        )

    def tearDown(self):
        """Need to remove all the csvs"""
        pass