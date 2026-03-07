from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
import os
import torch
from dotenv import load_dotenv
from alpaca_trade_api import REST
from timedelta import Timedelta
from finbert_utils import estimate_sentiment

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_API_SECRET")
BASE_URL = os.getenv("ALPACA_BASE_URL")

ALPACA_CREDS = {
    "API_KEY":API_KEY,
    "API_SECRET":API_SECRET,
    "PAPER": True
}

class MLTrader(Strategy):
    def initialize(self, symbol:str="SPY", cash_at_risk:float=0.5, take_profit=1.20, stop_loss = 0.95, momentum_days = 5):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk

        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.momentum_days = momentum_days

        self.api = REST(base_url=BASE_URL, secret_key=API_SECRET, key_id=API_KEY)

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price)
        return cash, last_price, quantity
    
    def get_dates(self):
        today = self.get_datetime()
        three_days_prior = today - Timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')

    def get_sentiment(self):
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=three_days_prior, end=today)
        
        news_list = [ev.headline for ev in news] 
        
        if not news_list:
            return 0, "neutral"

        probability, sentiment = estimate_sentiment(news_list)
        return probability, sentiment
    
    def get_momentum(self):
        bars = self.get_historical_prices(self.symbol, self.momentum_days, "day")
        prices = bars.df["close"]

        momentum = prices.iloc[-1] - prices.iloc[0]
        return momentum

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        probability, sentiment = self.get_sentiment()
        position = self.get_position(self.symbol)
        momentum = self.get_momentum()

        if cash > last_price: 
            if sentiment == "positive" and probability > 0.8 and position is None and momentum > 0: 
                if self.last_trade == "sell": 
                    self.sell_all() 

                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    "buy", 
                    type="bracket", 
                    take_profit_price=last_price*self.take_profit, 
                    stop_loss_price=last_price*self.stop_loss
                )
                self.submit_order(order) 
                self.last_trade = "buy"

            elif sentiment == "negative" and probability > 0.8 and position is None: 
                if self.last_trade == "buy": 
                    self.sell_all()

                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    "sell", 
                    type="bracket", 
                    take_profit_price=last_price*(2 - self.take_profit), 
                    stop_loss_price=last_price*(2 - self.stop_loss)
                )
                self.submit_order(order) 
                self.last_trade = "sell" 

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 1, 1)
broker = Alpaca(ALPACA_CREDS)
results = []

take_profit_values = [1.05, 1.10]
stop_loss_values = [0.95, 0.97]
momentum_values = [3,5]

for tp in take_profit_values:
    for sl in stop_loss_values:
        for momentum in momentum_values:

            print(f"Testing: TP={tp}, SL={sl}, Mom={momentum}")

            strategy = MLTrader(
                name=f'mlstrat_{tp}_{sl}_{momentum}',
                broker=broker, 
                parameters={
                    "symbol": "SPY",
                    "cash_at_risk": 0.5,
                    "take_profit": tp,
                    "stop_loss": sl,
                    "momentum_days": momentum
                }
            )
            
            result = strategy.backtest(
                YahooDataBacktesting,
                start_date,
                end_date,
                show_plot=False, 
                show_tearsheet=False, 
                save_tearsheet=False  
            )

            results.append((tp, sl, momentum, result))
best = max(results, key=lambda x: x[3]["total_return"])

print("\nBEST PARAMETERS FOUND")
print("Take Profit:", best[0])
print("Stop Loss:", best[1])
print("Momentum Days:", best[2])
print("Return:", best[3]["total_return"])