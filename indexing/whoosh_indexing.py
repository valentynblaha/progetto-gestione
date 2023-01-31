from whoosh.index import create_in
from whoosh.fields import *
import json
import os

schema = Schema(id=TEXT(stored=True), kind=TEXT, title=TEXT, user=TEXT(stored=True),
                likes=NUMERIC(int, stored=True), content=TEXT(phrase=True))
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
ix = create_in("indexdir", schema)

data_dir = os.path.join(os.getcwd(), 'data')
max_files = 50
i = 0
with ix.writer() as w:
    for filename in os.listdir(os.path.join(os.getcwd(), 'data')):
        print(f'Indexing file ({i}/{max_files}): {filename}')
        i += 1
        #if (i > max_files):
        #    break
        with w.group():
            with open(os.path.join(data_dir, filename), 'r') as f:
                video = json.loads(f.read())
            w.add_document(kind='video',
                           id=video['video']['id'],
                           title=video['video']['title'],
                           likes=video['video']['likes'],
                           content=video['video']['description'])
            for comment in video['comments']:
                w.add_document(kind='comment',
                               user=comment['topLevelComment']['author'],
                               likes=comment['topLevelComment']['likes'],
                               content=comment['topLevelComment']['text'])
