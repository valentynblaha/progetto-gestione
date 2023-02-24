#!/home/vale/dev/python/progetto-gestione/python_venv/bin/python3

import sys
from ysa.indexing import VideoSearcher

searcher = VideoSearcher('indexdir')

results = searcher.search(searcher.parse_query(sys.argv[1]))

print(f'Found {results.scored_length()} results')
for result in results:
    print(result, result.score)