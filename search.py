from ysa.indexing import VideoSearcher

searcher = VideoSearcher('indexdir')

results = searcher.search(searcher.parse_query('rust AND kind:comment AND negative:[0.3 TO]'))

print(f'Found {results.scored_length()} results')
for result in results:
    print(result, result.score)