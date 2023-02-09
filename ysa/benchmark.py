"""
Module for benchmarking the index using Discounted Cumulative Gain
"""
__all__ = ['calc_ndcg', 'get_video_list']

from sklearn.metrics import ndcg_score
from .indexing import VideoSearcher

import numpy as np

def get_dcg(relevance_list: list):
    if len(relevance_list) > 0:
        relevance_list[1:] = map(lambda x: x[1]/np.log2(x[0]), enumerate(relevance_list[1:], start=2))

        return sum(relevance_list)
    return 0


def calc_ndcg(ref_list: list, q_list: list):
    relevance_values = {}
    n = len(ref_list)
    for id in ref_list:
        relevance_values[id] = n
        n -= 1
    n = len(ref_list)
    true_relevance = [i for i in range(n, 0, -1)]
    q_relevance = [relevance_values.get(id) or 0 for id in q_list]
    if len(q_list) < n:
        q_relevance.extend((n- len(q_relevance)) * [0])
    elif len(q_list) > n:
        del q_relevance[n:]
    return get_dcg(q_relevance) / get_dcg(true_relevance)


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