from py5paisa import FivePaisaClient as Py5PaisaClient
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from config import config
import logging
import pandas as pd

logger = logging.getLogger(__name__)

class FivePaisaMarketData:
    """Real 5paisa API client for market data"""
    
    def __init__(self):
        self.client = None
        self.is_authenticated = False
        self.credentials = {
            "APP_NAME": config.FIVEPAISA_APP_NAME,
            "APP_SOURCE": config.FIVEPAISA_APP_SOURCE,
            "USER_ID": config.FIVEPAISA_USER_ID,
            "PASSWORD": config.FIVEPAISA_USER_PASSWORD,
            "USER_KEY": config.FIVEPAISA_USER_KEY,
            "ENCRYPTION_KEY": config.FIVEPAISA_ENCRYPTION_KEY
        }
        self.email = config.FIVEPAISA_EMAIL
        self.dob = config.FIVEPAISA_DOB
        
        # NSE F&O scrip codes (sample - expand as needed)
        self.scrip_codes = {
            'NIFTY': 999920000,
            'HDFCBANK': 1333,
            'ICICIBANK': 4963,
            'AXISBANK': 5900,
            'KOTAKBANK': 1922,
            'SBIN': 3045,
            'TCS': 11536,
            'INFY': 1594,
            'WIPRO': 3787,
            'RELIANCE': 2885,
            'TATAMOTORS': 3456,
            'M&M': 2031,
            'MARUTI': 10999,
            'BHARTIARTL': 10604,
            'ITC': 1660
        }
        
    async def initialize(self):
        """Initialize and login to 5paisa"""
        try:
            if not all([
                self.credentials["APP_NAME"],
                self.credentials["APP_SOURCE"],
                self.credentials["USER_ID"],
                self.credentials["PASSWORD"],
                self.credentials["USER_KEY"],
                self.credentials["ENCRYPTION_KEY"]
            ]):
                logger.warning("5paisa credentials incomplete. Using mock data.")
                return False
            
            # Initialize client with your actual credentials
            logger.info("Connecting to 5paisa with your credentials...")
            self.client = Py5PaisaClient(cred=self.credentials)
            
            # Try to get client code to verify connection
            try:
                client_code = self.client.get_client_code()
                logger.info(f"✅ SUCCESS! Connected to 5paisa. Client Code: {client_code}")
                self.is_authenticated = True
                return True
            except Exception as auth_error:
                logger.error(f"5paisa authentication failed: {auth_error}")
                logger.warning("Falling back to mock data")
                self.is_authenticated = False
                return False
            
        except Exception as e:
            logger.error(f"Failed to initialize 5paisa: {e}")
            logger.warning("Falling back to mock data")
            self.is_authenticated = False
            return False
    
    async def get_market_data(self, symbols: List[str], interval: str = "5min") -> Dict:
        """Get OHLC data for symbols"""
        if not self.is_authenticated or not self.client:
            logger.warning("5paisa not authenticated. Using mock data.")
            return self._get_mock_market_data(symbols)
        
        try:
            data = {}
            today = datetime.now()
            from_date = (today - timedelta(days=1)).strftime('%Y-%m-%d')
            to_date = today.strftime('%Y-%m-%d')
            
            # Map interval
            timeframe_map = {
                '5min': '5m',
                '15min': '15m',
                '1hour': '60m',
                '1day': '1d'
            }
            tf = timeframe_map.get(interval, '5m')
            
            for symbol in symbols:
                try:
                    scrip_code = self.scrip_codes.get(symbol)
                    if not scrip_code:
                        logger.warning(f"Scrip code not found for {symbol}")
                        continue
                    
                    # Fetch historical data
                    df = self.client.historical_data(
                        'N',  # NSE
                        'C',  # Cash (use 'D' for derivatives)
                        scrip_code,
                        tf,
                        from_date,
                        to_date
                    )
                    
                    if df is not None and not df.empty:
                        latest = df.iloc[-1]
                        data[symbol] = {
                            'open': float(latest['Open']),
                            'high': float(latest['High']),
                            'low': float(latest['Low']),
                            'close': float(latest['Close']),
                            'volume': int(latest['Volume']),
                            'vwap': float((latest['High'] + latest['Low'] + latest['Close']) / 3),
                            'timestamp': datetime.now()
                        }
                        logger.info(f"✓ Fetched data for {symbol}: Close={latest['Close']}")
                    
                except Exception as e:
                    logger.error(f"Error fetching {symbol}: {e}")
                    continue
            
            # If we got some real data, return it; otherwise use mock
            if data:
                return data
            else:
                logger.warning("No real data fetched. Using mock data.")
                return self._get_mock_market_data(symbols)
                
        except Exception as e:
            logger.error(f"Error in get_market_data: {e}")
            return self._get_mock_market_data(symbols)
    
    async def get_option_chain(self, symbol: str) -> Dict:
        """Get option chain data - using mock for now as py5paisa doesn't have direct method"""
        # Note: 5paisa Xstream API has option chain, but py5paisa library doesn't expose it directly
        # This would require custom API calls to Xstream endpoints
        logger.info(f"Option chain for {symbol} - using mock data (Xstream integration pending)")
        return self._get_mock_option_chain(symbol)
    
    async def get_nifty_data(self) -> Dict:
        """Get Nifty 50 index data"""
        return await self.get_market_data(["NIFTY"])
    
    def _get_mock_market_data(self, symbols: List[str]) -> Dict:
        """Generate mock market data for testing"""
        import random
        
        data = {}
        for symbol in symbols:
            base_price = random.uniform(800, 2000)
            data[symbol] = {
                'open': base_price,
                'high': base_price * 1.02,
                'low': base_price * 0.98,
                'close': base_price * random.uniform(0.99, 1.01),
                'volume': random.randint(100000, 1000000),
                'vwap': base_price * random.uniform(0.995, 1.005),
                'timestamp': datetime.now()
            }
        return data
    
    def _get_mock_option_chain(self, symbol: str) -> Dict:
        """Generate mock option chain data"""
        import random
        
        call_oi = random.randint(10000, 50000)
        put_oi = random.randint(10000, 50000)
        
        return {
            'symbol': symbol,
            'call_oi': call_oi,
            'put_oi': put_oi,
            'call_oi_change': random.randint(-5000, 5000),
            'put_oi_change': random.randint(-5000, 5000),
            'pcr': put_oi / call_oi if call_oi > 0 else 1.0,
            'timestamp': datetime.now()
        }
    
    async def close(self):
        """Close the API session"""
        if self.client:
            logger.info("Closing 5paisa session")
            self.client = None

# Singleton instance
market_data_client = FivePaisaMarketData()
