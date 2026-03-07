from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Tuple

device = "cuda:0" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)
labels = ["positive", "negative", "neutral"]


def estimate_sentiment(news_list):
    """
    Analyzes a list of headlines and returns a consensus score.
    Score ranges from -1 (total bearish) to 1 (total bullish).
    """
    if not news_list:
        return 0, "neutral"

    # 1. Batch tokenize all headlines at once
    tokens = tokenizer(news_list, return_tensors="pt", padding=True, truncation=True).to(device)
    
    with torch.no_grad():
        outputs = model(**tokens)
        logits = outputs.logits
        # Get probabilities for each headline
        probabilities = torch.nn.functional.softmax(logits, dim=-1)

    # 2. Count the votes
    # index: 0: positive, 1: negative, 2: neutral
    confidences, predictions = torch.max(probabilities, dim=-1)
    
    pos_count = torch.sum(predictions == 0).item()
    neg_count = torch.sum(predictions == 1).item()
    total = len(news_list)

    # 3. Calculate Consensus Score
    consensus_score = (pos_count - neg_count) / total
    
    # 4. Determine final sentiment label for the strategy
    if consensus_score > 0.2:
        final_sentiment = "positive"
    elif consensus_score < -0.2:
        final_sentiment = "negative"
    else:
        final_sentiment = "neutral"

    return abs(consensus_score), final_sentiment

if __name__ == "__main__":
    tensor, sentmiment = estimate_sentiment(['markets responded negatively to the news!','traders were displeased!'])
    print(tensor, sentmiment)
    print(torch.cuda.is_available())