from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
import os
from dotenv import load_dotenv

API_KEY = os.get("ALPACA_API_KEY")
API_SECRET = "ALPACA_API_SECRET"
BASE_URL = "ALPACA_BASE_URL"

ALPACA_CREDS = {
    "API_KEY":API_KEY,
    "API_SECRET":API_SECRET,
    "PAPER": True
}