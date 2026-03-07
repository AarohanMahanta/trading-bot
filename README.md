# ML Sentiment Trading Bot (FinBERT + Momentum)

An automated algorithmic trading system that combines **Natural Language Processing (NLP)** with quantitative price action to trade the S&P 500 ETF (SPY). 

The system uses **FinBERT** to distill market sentiment from live news headlines and filters entries based on price momentum to avoid "buying the dip" on negative news.

## 2023 Backtest Performance (Live Optimization)
The following results were generated from a full-year backtest (Jan 2023 - Dec 2023) using a **Persistent Disk Cache** to optimize inference speed.

| Metric | Strategy (ML Bot) | Benchmark (SPY) |
| :--- | :--- | :--- |
| **Annual Return** | 20.05% | 27.27% |
| **Max Drawdown** | -9.93% | -9.97% |
| **Sharpe Ratio** | 1.05 | 1.51 |
| **Win Days %** | 49.79% | 56.45% |
| **Correlation to S&P 500** | -0.04 | 1.00 |

### Analysis
* **Uncorrelated Alpha:** The bot achieved a **-0.04 correlation** to the benchmark, meaning it operates independently of broader market swings.
* **Risk Management:** The bot maintained a lower Max Drawdown than the S&P 500 during the testing period.
* **Efficiency:** Achieved 20.05% return while spending significantly less "Time in Market" than a Buy & Hold strategy.

---

## Strategy Logic

### 1. Sentiment Engine (NLP)
The bot fetches news headlines via the **Alpaca News API**. It utilizes **FinBERT** (a BERT model specialized for finance) to classify sentiment into Positive, Negative, or Neutral.

* **Consensus Logic:** We calculate a consensus score: 
$$\frac{\text{Positives} - \text{Negatives}}{\text{Total Headlines}}$$
* **Threshold:** A trade is only considered if the consensus probability exceeds **0.8**.

| Input Headline | Sentiment | Probability |
| :--- | :--- | :--- |
| "Markets rally after strong earnings" | Positive | 0.997 |

### 2. Execution (Bracket Orders)
The bot enters positions only when sentiment and momentum align, using **Bracket Orders** to manage risk:

* **Buy Trigger:** Positive Sentiment + Positive Momentum (Probability > 0.8).
* **Sell Trigger:** Negative Sentiment (Shorting) (Probability > 0.8).
* **Take Profit:** 7% ($1.07 \times \text{Price}$)
* **Stop Loss:** 7% ($0.93 \times \text{Price}$)

---

## Technical Architecture & Stack

**Machine Learning:**
* **Model:** `ProsusAI/finbert` (via HuggingFace Transformers).
* **Framework:** `LumiBot` for event-driven backtesting and live execution.

**Infrastructure:**
* **Broker API:** Alpaca Markets (Paper/Live).
* **Data Sources:** Yahoo Finance (Price) & Alpaca News API (Headlines).
* **Caching:** Custom **Persistent JSON KV Store** to cache sentiment analysis, reducing backtest duration by **95%**.

### Project Structure
```text
trading-bot/
│
├── trading_bot.py        # Main trading strategy and execution logic
├── finbert_utils.py      # Sentiment analysis and model inference module
├── .env                  # API credentials (ignored by git)
├── requirements.txt      # Project dependencies
└── README.md             # Documentation
```


## Setup
### 1. Installation

Clone the repo and install dependencies:

```text
pip install -r requirements.txt
```


### 2. Configuration

Set up your .env file with your Alpaca API keys:
```text
ALPACA_API_KEY=your_key_here
ALPACA_SECRET_KEY=your_secret_here
IS_PAPER=True
```
### 3. Usage

Run the backtest or optimization:
```text
python trading_bot.py
```

## License
This project is licensed under the **MIT License**.
