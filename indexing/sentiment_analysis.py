from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import os
import pickle
import hashlib

# load model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"

model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)



class SentimentAnalizer():

    #TODO: use binary instead of json
    __cache_filename = 'cache/sentiment_analysis.cache'
    __cache_dict = {}
    __cache_file = None

    def __init__(self) -> None:
        if not os.path.exists('cache'):
            os.mkdir('cache')
        if os.path.exists(self.__cache_filename):
            with open(self.__cache_filename, 'rb') as f:
                try:
                    self.__cache_dict = pickle.loads(f.read())
                except:
                    pass

    def score_text(self, text):
        if not self.__cache_file:
            self.__cache_file = open(self.__cache_filename, 'wb')
        encoded_text = tokenizer(text, return_tensors='pt')
        try:
            output = model(**encoded_text)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores).tolist()
        except:
            # Assign neutral score if scoring fails for some reasons
            scores = [0,1,0]
        return scores


    def get_score(self, text):
        hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        score = self.__cache_dict.get(hash)
        if score is None:
            score = self.score_text(text)
            self.__cache_dict[hash] = score
        return score

    
    def __del__(self):
        if self.__cache_file is not None:
            self.__cache_file.write(pickle.dumps(self.__cache_dict))
            self.__cache_file.close()
