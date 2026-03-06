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
Momentum Indicator

The strategy also calculates short term price momentum:
Momentum = Price(today) - Price(N days ago)
This prevents the bot from buying when sentiment is positive but the price trend is falling.
Risk Management
Each trade uses bracket orders.
A bracket order automatically creates:
Take Profit
Stop Loss
Example:
Buy SPY at $100

Take Profit → $120
Stop Loss → $95
This protects against large losses and locks in gains automatically.
Parameter Optimization
The system also includes a parameter optimization engine.
It tests multiple combinations of:
Take Profit %
Stop Loss %
Momentum Window
Example search grid:
Take Profit: 1.05, 1.10
Stop Loss: 0.95, 0.97
Momentum Days: 3, 5
Each configuration is backtested to determine the best performing strategy.
Example Output
Testing: 1.05 0.95 3
Testing: 1.05 0.95 5
Testing: 1.10 0.97 3
...

BEST PARAMETERS FOUND
Take Profit: 1.10
Stop Loss: 0.95
Momentum Days: 5
Return: 0.18
Installation
Clone the repository:
git clone https://github.com/yourusername/ml-sentiment-trading-bot
cd ml-sentiment-trading-bot
Install dependencies:
pip install -r requirements.txt
Environment Variables
Create a .env file:
ALPACA_API_KEY=your_key
ALPACA_API_SECRET=your_secret
ALPACA_BASE_URL=https://paper-api.alpaca.markets
Running the Bot
Run backtesting:
python trading_bot.py
The system will simulate trades using historical market data.
Disclaimer
This project is for educational purposes only.
It does not constitute financial advice and should not be used to make real investment decisions.
Trading involves risk and past performance does not guarantee future results.
Possible Future Improvements
Portfolio trading (multiple assets)
Reinforcement learning strategies
Real-time market streaming
News filtering with LLMs
Risk-adjusted position sizing
Performance dashboards
License
MIT License
