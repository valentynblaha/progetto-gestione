from ysa.indexing import VideoSearcher
from ysa.utils import print_yellow
from ysa.benchmark import *

with open('queries.txt', 'r') as f:
    searcher = VideoSearcher('indexdir')
    queries = f.read().splitlines()
    for i, query in enumerate(queries):
        print_yellow('Result for query: ', query)
        q_list = get_video_list(query, searcher)
        try:
            with open(f'queries_dcg/{i + 1}.txt', 'r') as qf:
                ref_list = qf.read().splitlines()
                print('Ref list: ', ref_list)
            ndcg = calc_ndcg(ref_list, q_list)
        except:
            ndcg = 1
        finally:
            print(f'Query {i + 1} nDCG score: {ndcg}')