from indexing.whoosh_searching import VideoSearcher
import json

searcher = VideoSearcher('indexdir')

results = searcher.search(searcher.parse_query('kind:video AND solidity AND publishedAt:[7 feb 2021 TO]'))

print(f'Found {results.scored_length()} results')
for result in results:
    print(result, result.score)