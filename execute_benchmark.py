from ysa.indexing import VideoSearcher
from ysa.utils import print_yellow, print_red
from ysa.benchmark import *

with open('benchmarking/queries.txt', 'r') as f:
    searcher = VideoSearcher('indexdir')
    queries = f.read().splitlines()
    values = []
    for i, query in enumerate(queries):
        print_yellow('Result for query: ', query)
        q_list = get_video_list(query, searcher)
        try:
            with open(f'benchmarking/queries_dcg/{i + 1}.txt', 'r') as qf:
                ref_list = qf.read().splitlines()
                #print('Ref list: ', ref_list)
            ndcg = calc_ndcg(ref_list, q_list)
            values.append(ndcg)
        except Exception as e:
            print_red(e)
            ndcg = 1
        finally:
            print(f'Query {i + 1} nDCG score: {ndcg}')
    print('\nMean nDCG score: ', sum(values) / len(values))