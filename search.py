from indexing.whoosh_searching import VideoSearcher
import json

searcher = VideoSearcher('indexdir')

results = searcher.search(searcher.parse_query('javascript AND positive:[0.5 TO]'))

for result in results:
    print(result.get('id'))