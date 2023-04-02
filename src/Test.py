# tested in transformers==4.18.0
from transformers import BertTokenizer, BertForSequenceClassification, pipeline

finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
nlp = pipeline("text-classification", model=finbert, tokenizer=tokenizer)
results = nlp('Roblox is doing really bad and is underperforming.')
print(results)  # [{'label': 'Positive', 'score': 1.0}]
