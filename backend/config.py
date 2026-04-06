import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

class Config:
    # MongoDB
    MONGO_URL = os.environ['MONGO_URL']
    DB_NAME = os.environ['DB_NAME']
    
    # 5paisa API
    FIVEPAISA_APP_NAME = os.getenv('FIVEPAISA_APP_NAME', '')
    FIVEPAISA_APP_SOURCE = os.getenv('FIVEPAISA_APP_SOURCE', '')
    FIVEPAISA_USER_ID = os.getenv('FIVEPAISA_USER_ID', '')
    FIVEPAISA_USER_PASSWORD = os.getenv('FIVEPAISA_USER_PASSWORD', '')
    FIVEPAISA_USER_KEY = os.getenv('FIVEPAISA_USER_KEY', '')
    FIVEPAISA_ENCRYPTION_KEY = os.getenv('FIVEPAISA_ENCRYPTION_KEY', '')
    FIVEPAISA_EMAIL = os.getenv('FIVEPAISA_EMAIL', 'user@example.com')
    FIVEPAISA_DOB = os.getenv('FIVEPAISA_DOB', '19900101')
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    
    # Email
    GMAIL_SENDER = os.getenv('GMAIL_SENDER', '')
    GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', '')
    EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS', '').split(',')
    
    # News API
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
    
    # Trading
    RISK_PER_TRADE = float(os.getenv('RISK_PER_TRADE', 0.01))
    MAX_CONCURRENT_TRADES = int(os.getenv('MAX_CONCURRENT_TRADES', 3))
    MIN_SIGNAL_SCORE = int(os.getenv('MIN_SIGNAL_SCORE', 8))
    
    # Sectors
    SECTORS = {
        'BANKING': ['HDFCBANK', 'ICICIBANK', 'AXISBANK', 'KOTAKBANK', 'SBIN'],
        'IT': ['TCS', 'INFY', 'WIPRO', 'HCLTECH', 'TECHM'],
        'AUTO': ['MARUTI', 'M&M', 'TATAMOTORS', 'BAJAJ-AUTO', 'HEROMOTOCO'],
        'FMCG': ['HINDUNILVR', 'ITC', 'NESTLEIND', 'BRITANNIA', 'DABUR'],
        'METALS': ['TATASTEEL', 'HINDALCO', 'JSWSTEEL', 'VEDL', 'COALINDIA']
    }

config = Config()