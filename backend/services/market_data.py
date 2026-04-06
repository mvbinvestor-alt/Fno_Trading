import httpx
from typing import List, Dict, Optional
from datetime import datetime
from config import config
import logging

logger = logging.getLogger(__name__)

class FivePaisaClient:
    """5paisa API client for market data"""
    
    def __init__(self):
        self.api_key = config.FIVEPAISA_API_KEY
        self.secret_key = config.FIVEPAISA_SECRET_KEY
        self.client_id = config.FIVEPAISA_CLIENT_ID
        self.base_url = "https://openapi.5paisa.com/VendorsAPI/Service1.svc"
        self.session = None
        
    async def initialize(self):
        """Initialize API session"""
        if not all([self.api_key, self.secret_key, self.client_id]):
            logger.warning("5paisa credentials not configured. Using mock data.")
            return False
        
        try:
            # TODO: Implement actual 5paisa authentication
            # This is a placeholder for 5paisa login
            self.session = httpx.AsyncClient()
            return True
        except Exception as e:
            logger.error(f"Failed to initialize 5paisa client: {e}")
            return False
    
    async def get_market_data(self, symbols: List[str], interval: str = "5min") -> Dict:
        """Get OHLC data for symbols"""
        if not self.session:
            # Return mock data if not initialized
            return self._get_mock_market_data(symbols)
        
        try:
            # TODO: Implement actual 5paisa market data API call
            # Placeholder implementation
            return self._get_mock_market_data(symbols)
        except Exception as e:
            logger.error(f"Error fetching market data: {e}")
            return self._get_mock_market_data(symbols)
    
    async def get_option_chain(self, symbol: str) -> Dict:
        """Get option chain data for a symbol"""
        if not self.session:
            return self._get_mock_option_chain(symbol)
        
        try:
            # TODO: Implement actual 5paisa option chain API call
            return self._get_mock_option_chain(symbol)
        except Exception as e:
            logger.error(f"Error fetching option chain: {e}")
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
        if self.session:
            await self.session.aclose()

# Singleton instance
market_data_client = FivePaisaClient()