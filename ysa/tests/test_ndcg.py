from ..benchmark import calc_ndcg, get_dcg

import unittest

class TestNDCG(unittest.TestCase):

    def test1(self):
        ref_list = ['d4', 'd3', 'd2', 'd1']
        q_list = ['d3', 'd2', 'd4', 'd1']

        self.assertAlmostEqual(calc_ndcg(ref_list, q_list), 0.9157552695001, 10)

    
    def test2(self):
        r_list = [4, 3, 2, 1]
        self.assertAlmostEqual(get_dcg(r_list), 8.7618595071429, 10)