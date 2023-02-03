from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# load model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"

model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

def score_text(text):
    encoded_text = tokenizer(text, return_tensors='pt')
    try:
        output = model(**encoded_text)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
    except:
        # Assign neutral score if scoring fails for some reasons
        scores = [0,1,0]
    return scores