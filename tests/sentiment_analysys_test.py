from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import os
import json

video_id = 'wTuymXD0mNE'
roberta = "cardiffnlp/twitter-roberta-base-sentiment"

model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ['Negative', 'Neutral', 'Positive']

YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

with open(os.path.join(os.getcwd(), f'data/{video_id}.json'), 'r') as f:
    json_data = json.loads(f.read())

    comments = [comment['topLevelComment'] for comment in json_data['comments']]
    i = 0
    for comment in comments:
        i += 1
        text = comment['text']
        encoded_comment = tokenizer(text, return_tensors='pt')
        try:
            output = model(**encoded_comment)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
        except:
            # Error fix
            # scores = [0, 1, 0]
            continue
        
        print(f'{YELLOW}Comment {i}{NC}')
        print(text)
        print('Scores: ', scores)