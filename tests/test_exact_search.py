import unittest
import os


class ExactSearch(unittest.TestCase):
    # Deve ritornare True o False
    
    def test1(self):
        ids = ['rfscVS0vtbw', 
            '-h7gOJbIpmo', 
            'GhQdlIFylQ8', 
            'VPvVD8t02U8', 
            'pQN-pnXPaVg', 
            '025QFeZfeyM', 
            'OK_JCtrrv-c', 
            'M576WGiDBdQ', 
            'zOjov-2OZ0E', 
            'fmyvWz5TUWg']
        query = 'developing'
        for id in ids:
            with open(os.path.join(os.getcwd(), f'data/{id}.json'), 'r') as f:
                text = f.read()
                self.assertTrue(query in text.lower())


    def test2(self):
        ids = ['HXV3zeQKqGY']
        query = 'gatto'
        for id in ids:
            with open(os.path.join(os.getcwd(), f'data/{id}.json'), 'r') as f:
                text = f.read()
                self.assertTrue(query in text.lower())