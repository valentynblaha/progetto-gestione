"""
Module for benchmarking the index using Discounted Cumulative Gain
"""
__all__ = ['calc_ndcg', 'get_video_list']

import numpy as np

from .indexing import VideoSearcher


def get_dcg(relevance_list: list):
    """Calculate Discounted Cumulative Gain for a list of relevance values

    Args:
        relevance_list (list): List of relevance values

    Returns:
        number: Discounted Cumulative Gain
    """
    if len(relevance_list) > 0:
        relevance_list[1:] = map(lambda x: x[1]/np.log2(x[0]), enumerate(relevance_list[1:], start=2))

        return sum(relevance_list)
    return 0


def calc_ndcg(ref_list: list, q_list: list):
    """Given two lists of documents calculates the normalized discounted
    cumulative gain of the list `q_list` with respect to a reference list `ref_list`

    Args:
        ref_list (list): Reference list. Contains the expected ranking of documents
        q_list (list): Testing list. Contains the documents as ranked by the testing model

    Returns:
        number: Ranges from 0.0 to 1.0 - Normalized discounted cumulative gain
    """
    relevance_values = {}
    n = len(ref_list)
    for document in ref_list:
        relevance_values[document] = n
        n -= 1
    n = len(ref_list)
    true_relevance = list(range(n, 0, -1))
    q_relevance = [relevance_values.get(id) or 0 for id in q_list]
    if len(q_list) < n:
        q_relevance.extend((n- len(q_relevance)) * [0])
    elif len(q_list) > n:
        del q_relevance[n:]
    return get_dcg(q_relevance) / get_dcg(true_relevance)


def get_video_list(query, searcher: VideoSearcher):
    """Given a search query (to be parsed by Whoosh) and a VideoSearcher
    returns the list of documents that contain the results returned by the searcher
    while mantaining the ranking order.

    Args:
        query (str): Query (using the Whoosh default query language)
        searcher (VideoSearcher): VideoSearcher object that executes the search

    Returns:
        list: Documents returned by the searcher
    """
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
