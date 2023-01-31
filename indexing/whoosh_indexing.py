from whoosh.index import create_in
from whoosh.fields import *
import json
import os

schema = Schema(id=TEXT(stored=True), kind=TEXT, user=TEXT(stored=True),
                likes=NUMERIC(int, stored=True), content=TEXT)
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
        if (i > max_files):
            break
        with w.group():
            with open(os.path.join(data_dir, filename), 'r') as f:
                data = json.loads(f.read())
            w.add_document(kind='video',
                           id=data['video']['id'],
                           likes=data['video']['likes'],
                           content=data['video']['description'])
            for comment in data['comments']:
                w.add_document(kind='comment',
                               user=comment['topLevelComment']['author'],
                               likes=comment['topLevelComment']['likes'],
                               content=comment['topLevelComment']['text'])
