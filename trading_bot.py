import os
from datetime import datetime
from dotenv import load_dotenv
from alpaca_trade_api import REST
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from timedelta import Timedelta
from finbert_utils import estimate_sentiment
import warnings
warnings.filterwarnings('ignore')

load_dotenv()
ALPACA_CREDS = {
    "API_KEY": os.getenv("ALPACA_API_KEY"),
    "API_SECRET": os.getenv("ALPACA_API_SECRET"),
    "PAPER": True
}

class MLTrader(Strategy):
    def initialize(self, symbol: str = "SPY", cash_at_risk: float = 1.0, 
                   take_profit=1.07, stop_loss=0.93, momentum_days=1):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.momentum_days = momentum_days
        self.trades_made = 0
        self.prev_close = None
        self.api = REST(base_url=os.getenv("ALPACA_BASE_URL"), 
                        secret_key=os.getenv("ALPACA_API_SECRET"), 
                        key_id=os.getenv("ALPACA_API_KEY"))

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        if last_price is None or last_price == 0:
            return 0, 0, 0
        quantity = round(cash * self.cash_at_risk / last_price, 0)
        return cash, last_price, int(quantity)
    
    def get_dates(self):
        today = self.get_datetime()
        three_days_prior = today - Timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')

    def get_sentiment(self):
        today, three_days_prior = self.get_dates()
        try:
            news = self.api.get_news(symbol=self.symbol, start=three_days_prior, end=today)
            news_list = [ev.headline for ev in news] if news else []
            if not news_list:
                return 0.5, "neutral"
            probability, sentiment = estimate_sentiment(news_list, cache_key=today)
            return probability, sentiment
        except:
            return 0.5, "neutral"

    def get_momentum(self):
        try:
            bars = self.get_historical_prices(self.symbol, 1, "day")
            if bars is None or bars.df is None or bars.df.empty:
                return 0
            prices = bars.df["close"]
            if len(prices) < 1:
                return 0
            if self.prev_close is not None:
                momentum_pct = (float(prices.iloc[-1]) - self.prev_close) / self.prev_close
            else:
                momentum_pct = 0
            self.prev_close = float(prices.iloc[-1])
            return momentum_pct
        except:
            return 0

    def on_trading_iteration(self):
        try:
            cash, last_price, quantity = self.position_sizing()
            if quantity <= 0 or last_price <= 0:
                return
                
            probability, sentiment = self.get_sentiment()
            position = self.get_position(self.symbol)
            momentum = self.get_momentum()
            
            if position:
                if (position.side == "buy" and momentum < -0.01) or \
                   (position.side == "sell" and momentum > 0.01):
                    print(f"🟡 CLOSING position - momentum reversal")
                    self.sell_all()
                    return
            
            if cash > last_price * quantity and position is None:
                if sentiment in ["positive", "neutral"] and momentum > -0.005:
                    print(f"BUY: {sentiment} ({probability:.2f}) Mom: {momentum:.3f}")
                    order = self.create_order(
                        self.symbol, quantity, "buy", type="bracket",
                        take_profit_price=round(last_price * self.take_profit, 2),
                        stop_loss_price=round(last_price * self.stop_loss, 2)
                    )
                    self.submit_order(order)
                    self.trades_made += 1
                
                elif sentiment == "negative" and momentum < 0.005:
                    print(f"SELL: {sentiment} ({probability:.2f}) Mom: {momentum:.3f}")
                    order = self.create_order(
                        self.symbol, quantity, "sell", type="bracket",
                        take_profit_price=round(last_price * (2 - self.take_profit), 2),
                        stop_loss_price=round(last_price * (2 - self.stop_loss), 2)
                    )
                    self.submit_order(order)
                    self.trades_made += 1
                    
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 1, 1)
    
    params = {
        "take_profit": 1.07,
        "stop_loss": 0.93,
        "momentum_days": 1,
        "cash_at_risk": 1.0,
        "symbol": "SPY"
    }

    print("Running final strategy...")
    
    result = MLTrader.backtest(
        YahooDataBacktesting,
        start_date,
        end_date,
        parameters=params,
        show_plot=True,
        show_tearsheet=True
    )
    
    if result:
        total_return = result.get('total_return', 0)
        if isinstance(total_return, str):
            total_return = float(total_return.replace('%', ''))
        
        print("\n" + "="*50)
        print("Final Results:")
        print(f"Bot Return: {total_return:.2f}%")
        print(f"SPY Return: 27.00%")
        print("="*50)