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
- News sentiment is positive
- Sentiment probability > 0.8
- Momentum over the last N days is positive
- No existing position is open
When a buy signal occurs the bot places a bracket order:
BUY SPY
Take Profit: +X%
Stop Loss: -Y%
Example:
Buy at: $100
Take Profit: $110
Stop Loss: $95
### Sell (Short) Signal
The bot enters a short position when:
- News sentiment is negative
- Sentiment probability > 0.8
- No existing position is open
- The bot profits if the price falls.
## Key Technologies
This project uses several important technologies:
Machine Learning:
- HuggingFace Transformers
- FinBERT (financial sentiment analysis)
- Trading Infrastructure
- Lumibot trading framework
- Alpaca paper trading API
Data:
- Yahoo Finance historical price data
- Alpaca financial news API
Project Structure:
trading-bot/
│
├── trading_bot.py        # Main trading strategy
├── finbert_utils.py      # Sentiment analysis module
├── .env                  # API credentials
├── requirements.txt
└── README.md

## Sentiment Analysis
Sentiment analysis is performed using:
FinBERT
A BERT model trained specifically on financial text such as:
- earnings reports
- market news
- analyst commentary
  
The model classifies headlines into:
- Positive
- Negative
- Neutral
  
Example:
"Markets rally after strong earnings"


Sentiment: Positive

Probability: 0.997

MIT Licence
