from typing import Dict
import logging
from models import MarketRegime

logger = logging.getLogger(__name__)

class RegimeDetector:
    """Market regime detection based on Nifty 50"""
    
    def __init__(self):
        self.current_regime = MarketRegime.SIDEWAYS
    
    def detect_regime(self, nifty_data: Dict, market_breadth: Dict) -> MarketRegime:
        """Determine market regime"""
        try:
            # Extract data
            close = nifty_data.get('close', 0)
            vwap = nifty_data.get('vwap', 0)
            ad_ratio = market_breadth.get('ad_ratio', 1.0)
            
            bullish_signals = 0
            bearish_signals = 0
            
            # Check price vs VWAP
            if close > vwap:
                bullish_signals += 1
            elif close < vwap:
                bearish_signals += 1
            
            # Check A/D ratio
            if ad_ratio > 1.2:
                bullish_signals += 1
            elif ad_ratio < 0.8:
                bearish_signals += 1
            
            # Check trend (simplified - in production, use 15min chart)
            # Here we use close vs open as proxy
            if nifty_data.get('close', 0) > nifty_data.get('open', 0):
                bullish_signals += 1
            else:
                bearish_signals += 1
            
            # Determine regime
            if bullish_signals >= 2 and bearish_signals == 0:
                regime = MarketRegime.BULLISH
            elif bearish_signals >= 2 and bullish_signals == 0:
                regime = MarketRegime.BEARISH
            else:
                regime = MarketRegime.SIDEWAYS
            
            self.current_regime = regime
            logger.info(f"Market regime detected: {regime}")
            return regime
            
        except Exception as e:
            logger.error(f"Error detecting regime: {e}")
            return MarketRegime.SIDEWAYS
    
    def get_current_regime(self) -> MarketRegime:
        return self.current_regime

regime_detector = RegimeDetector()