from sklearn.metrics import ndcg_score, dcg_score
import numpy as np
from indexing.whoosh_searching import VideoSearcher

def calc_ndcg(ref_list, q_list):

    relevance_values = {}
    n = len(ref_list)
    for id in ref_list:
        relevance_values[id] = n
        n -= 1
    n = len(ref_list)
    true_relevance = np.asarray([[i for i in range(n, 0, -1)]])
    q_relevance = [relevance_values.get(id) or 0 for id in q_list]
    if len(q_list) < n:
        q_relevance.extend((n- len(q_relevance)) * [0])
    elif len(q_list) > n:
        del q_relevance[n:]
    relevance_score = np.asarray([q_relevance])

    return ndcg_score(true_relevance, relevance_score)
    

def get_video_list(query, searcher: VideoSearcher):
    results = searcher.search(searcher.parse_query(query))

    print(f'Found {results.scored_length()} results')
    video_ids = []
    for result in results:
        if result.get('kind') == 'video':
            video_ids.append(result.get('id'))
        elif result.get('kind') == 'comment':
            video_id = result.get('videoId')
            if video_id not in video_ids:
                video_ids.append(video_id)
    #print(video_ids)
    return video_ids


def print_yellow(*args, **kwargs):
    YELLOW='\033[1;33m'
    NC='\033[0m' # No Color
    print(YELLOW, *args, NC, **kwargs)


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