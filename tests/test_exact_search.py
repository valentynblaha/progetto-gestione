import unittest


class ExactSearch(unittest.TestCase):
    
    def check_query(self, ids, query):
        for id in ids:
            with open(f'data/{id}.json', 'r') as f:
                text = f.read()
                self.assertTrue(query in text.lower())


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
        self.check_query(ids, query)


    def test2(self):
        ids = ['HXV3zeQKqGY']
        query = 'gatto'
        self.check_query(ids, query)