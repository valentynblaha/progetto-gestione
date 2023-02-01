from whoosh.index import create_in
from whoosh.fields import *
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import json
import os

schema = Schema(id=TEXT(stored=True), kind=TEXT, title=TEXT, user=TEXT(stored=True),
                likes=NUMERIC(int, stored=True), content=TEXT(phrase=True), positive=NUMERIC(float, stored=True),
                neutral=NUMERIC(float, stored=True), negative=NUMERIC(float, stored=True))
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
ix = create_in("indexdir", schema)

data_dir = os.path.join(os.getcwd(), 'data')
max_files = 10
i = 0

# load model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"

model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ['Negative', 'Neutral', 'Positive']

with ix.writer() as w:
    for filename in os.listdir(os.path.join(os.getcwd(), 'data')):
        i += 1
        print(f'Indexing file ({i}/{max_files}): {filename}')
        if (i > max_files):
            break
        with w.group():
            with open(os.path.join(data_dir, filename), 'r') as f:
                video = json.loads(f.read())
            w.add_document(kind='video',
                           id=video['video']['id'],
                           title=video['video']['title'],
                           likes=video['video']['likes'],
                           content=video['video']['description'])
            for comment in video['comments']:
                # TODO: include replies as well
                text = comment['topLevelComment']['text']
                encoded_comment = tokenizer(text, return_tensors='pt')
                try:
                    output = model(**encoded_comment)
                    scores = output[0][0].detach().numpy()
                    scores = softmax(scores)
                except:
                    scores = [0,1,0]
                # print(encoded_tweet)
                w.add_document(kind='comment',
                               user=comment['topLevelComment']['author'],
                               likes=comment['topLevelComment']['likes'],
                               content=text,
                               negative=scores[0],
                               neutral=scores[1],
                               positive=scores[2])
