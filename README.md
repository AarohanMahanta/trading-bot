# ML Sentiment Trading Bot

A machine learning powered trading bot that uses financial news sentiment and momentum analysis to trade the S&P 500 ETF automatically.

The system combines natural language processing (FinBERT) with quantitative trading strategies to make buy and sell decisions based on market sentiment extracted from news headlines.

## Overview
This project implements a fully automated trading strategy that:
- Collects financial news related to a target asset.
- Uses a pretrained financial NLP model (FinBERT) to determine market sentiment.
- Combines sentiment with price momentum indicators.
- Executes simulated trades using Alpaca's paper trading API.
- Uses bracket orders with stop-loss and take-profit risk management.
- Backtests strategies on historical data to evaluate performance.
- Performs parameter optimization to find the best trading configuration.

## Strategy Logic
The bot trades the ETF SPY (which tracks the S&P 500).

### Buy Signal
The bot enters a long position when:
- News sentiment is positive.
- Sentiment probability > 0.8.
- Momentum over the last N days is positive.
- No existing position is open.

When a buy signal occurs, the bot places a bracket order:
- **Action:** BUY SPY
- **Take Profit:** +X%
- **Stop Loss:** -Y%

### Sell (Short) Signal
The bot enters a short position when:
- News sentiment is negative.
- Sentiment probability > 0.8.
- No existing position is open.
- The bot profits if the price falls.

## Key Technologies
This project integrates the following stacks:

**Machine Learning:**
- HuggingFace Transformers
- FinBERT (specialized financial sentiment analysis)

**Trading Infrastructure:**
- Lumibot trading framework
- Alpaca paper trading API

**Data Sources:**
- Yahoo Finance (historical price data)
- Alpaca News API (financial news headlines)

## Project Structure
```text
trading-bot/
│
├── trading_bot.py        # Main trading strategy and execution logic
├── finbert_utils.py      # Sentiment analysis and model inference module
├── .env                  # API credentials (ignored by git)
├── requirements.txt      # Project dependencies
└── README.md             # Documentation
```
## Sentiment Analysis
Sentiment analysis is performed using **FinBERT**, a specialized BERT model pre-trained on a massive corpus of financial text. This training data includes earnings reports, market news, and analyst commentary, allowing the model to understand the specific nuances of financial language.

### Model Classification
The model analyzes each headline and classifies it into one of three categories:
* **Positive**
* **Negative**
* **Neutral**

### Example Processing
The bot processes news strings and returns the dominant sentiment along with a confidence score.

| Input Headline | Sentiment | Probability |
| :--- | :--- | :--- |
| "Markets rally after strong earnings" | Positive | 0.997 |



---

## License
This project is licensed under the **MIT License**.
