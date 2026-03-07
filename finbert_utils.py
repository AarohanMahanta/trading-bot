from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Tuple, List
import warnings
warnings.filterwarnings('ignore')

device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device} for sentiment analysis")

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)
model.eval()
labels = ["positive", "negative", "neutral"]

_sentiment_cache = {}

def estimate_sentiment(news_list: List[str], cache_key=None) -> Tuple[float, str]:
    """
    Analyzes news headlines and returns sentiment probability and label
    """
    if cache_key and cache_key in _sentiment_cache:
        return _sentiment_cache[cache_key]
    
    if not news_list:
        return 0.0, "neutral"

    try:
        tokens = tokenizer(news_list, return_tensors="pt", padding=True, 
                          truncation=True, max_length=512).to(device)
        
        with torch.no_grad():
            outputs = model(**tokens)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)

        avg_probabilities = probabilities.mean(dim=0)
        
        max_prob, max_idx = torch.max(avg_probabilities, dim=0)
        sentiment = labels[max_idx]
        
        if sentiment == "neutral" and max_prob < 0.6:
            sentiment = "neutral"
            probability = 0.5
        else:
            probability = float(max_prob)

        result = (probability, sentiment)

        if cache_key:
            _sentiment_cache[cache_key] = result
        
        return result
        
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return 0.5, "neutral"

if __name__ == "__main__":
    test_headlines = [
        'markets responded positively to strong earnings',
        'traders optimistic about fed policy'
    ]
    prob, sent = estimate_sentiment(test_headlines)
    print(f"Probability: {prob:.2f}, Sentiment: {sent}")