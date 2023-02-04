from whoosh.index import create_in
from whoosh.fields import *
import json
import os
import dateutil.parser
import sentiment_analysis
import numpy

schema = Schema(id=STORED,
                kind=ID,
                publishedAt=DATETIME,
                title=TEXT(field_boost=2, analyzer=analysis.StemmingAnalyzer()),
                user=ID(stored=True),
                likes=NUMERIC(int, stored=True),
                content=TEXT(phrase=True, analyzer=analysis.StemmingAnalyzer()),
                positive=NUMERIC(float, stored=True),
                neutral=NUMERIC(float, stored=True),
                negative=NUMERIC(float, stored=True))
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
ix = create_in("indexdir", schema)

data_dir = os.path.join(os.getcwd(), 'data')
max_files = 20
i = 0

sentiment_analyzer = sentiment_analysis.SentimentAnalizer()

def add_comment(writer, comment):
    text = comment['text']
    scores = sentiment_analyzer.get_score(text)
    writer.add_document(id=comment['id'],
                    kind='comment',
                    publishedAt=dateutil.parser.isoparse(comment['publishedAt']),
                    user=comment['author'],
                    likes=comment['likes'],
                    content=text,
                    negative=scores[0],
                    neutral=scores[1],
                    positive=scores[2])
    return scores

def index_video(writer, path):
    
    with open(path, 'r') as f:
        video = json.loads(f.read())
    L = 0
    video_scores = numpy.zeros(3)
    for comment in video['comments']:
        scores = add_comment(w, comment['topLevelComment'])
        weight = comment['topLevelComment']['likes'] + 1
        video_scores += numpy.array(scores) * weight
        L += weight
        if replies := comment.get('replies'):
            for reply in replies:
                add_comment(w, reply)
    video_scores /= L
    writer.add_document(kind='video',
                    id=video['video']['id'],
                    publishedAt=dateutil.parser.isoparse(video['video']['publishedAt']),
                    title=video['video']['title'],
                    likes=video['video']['likes'],
                    content=video['video']['description'],
                    negative=video_scores[0],
                    neutral=video_scores[1],
                    positive=video_scores[2]
                    )

with ix.writer() as w:
    for filename in os.listdir(os.path.join(os.getcwd(), 'data')):
        i += 1
        print(f'Indexing file ({i}/{max_files}): {filename}')
        # For debugging
        if (i >= max_files):
            break
        with w.group():
            index_video(w, os.path.join(data_dir, filename))