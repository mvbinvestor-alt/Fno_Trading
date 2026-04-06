from typing import Dict, List, Optional
import logging
from models import Signal, SignalType, MarketRegime
from config import config
import talib
import numpy as np

logger = logging.getLogger(__name__)

class PriceActionStrategy:
    """High-probability price action setups"""
    
    def identify_long_setup(self, stock: str, data: Dict, regime: MarketRegime, 
                           sector: str, option_signal: str) -> Optional[Dict]:
        """Identify LONG setup conditions"""
        try:
            # Must be in bullish regime
            if regime != MarketRegime.BULLISH:
                return None
            
            close = data['close']
            open_price = data['open']
            high = data['high']
            low = data['low']
            vwap = data.get('vwap', close)
            volume = data['volume']
            
            reasons = []
            score = 0
            
            # Check if stock is above VWAP
            if close < vwap:
                return None
            
            reasons.append("Above VWAP")
            score += 1
            
            # Check for bullish candle pattern
            body = abs(close - open_price)
            total_range = high - low
            
            if close > open_price and body / total_range > 0.6:
                reasons.append("Strong bullish candle")
                score += 2
            
            # Volume check (simplified - needs historical avg)
            if volume > 100000:  # Placeholder
                reasons.append("Volume spike")
                score += 1
            
            # Option chain alignment
            if option_signal == "BULLISH":
                reasons.append("Option chain bullish")
                score += 2
            
            # Valid setup
            if score >= 4:
                # Calculate levels
                entry = high + (high * 0.002)  # Breakout entry
                stop_loss = low * 0.995  # Below pullback low
                
                # Risk-reward targets
                risk = entry - stop_loss
                target_1 = entry + (risk * 1.5)
                target_2 = entry + (risk * 2.0)
                
                return {
                    'stock': stock,
                    'signal_type': SignalType.LONG,
                    'entry': round(entry, 2),
                    'stop_loss': round(stop_loss, 2),
                    'target_1': round(target_1, 2),
                    'target_2': round(target_2, 2),
                    'score': score,
                    'reasons': reasons,
                    'sector': sector
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error identifying long setup for {stock}: {e}")
            return None
    
    def identify_short_setup(self, stock: str, data: Dict, regime: MarketRegime,
                            sector: str, option_signal: str) -> Optional[Dict]:
        """Identify SHORT setup conditions"""
        try:
            # Must be in bearish regime
            if regime != MarketRegime.BEARISH:
                return None
            
            close = data['close']
            open_price = data['open']
            high = data['high']
            low = data['low']
            vwap = data.get('vwap', close)
            volume = data['volume']
            
            reasons = []
            score = 0
            
            # Check if stock is below VWAP
            if close > vwap:
                return None
            
            reasons.append("Below VWAP")
            score += 1
            
            # Check for bearish candle pattern
            body = abs(close - open_price)
            total_range = high - low
            
            if close < open_price and body / total_range > 0.6:
                reasons.append("Strong bearish candle")
                score += 2
            
            # Volume check
            if volume > 100000:
                reasons.append("Volume spike")
                score += 1
            
            # Option chain alignment
            if option_signal == "BEARISH":
                reasons.append("Option chain bearish")
                score += 2
            
            # Valid setup
            if score >= 4:
                # Calculate levels
                entry = low - (low * 0.002)  # Breakdown entry
                stop_loss = high * 1.005  # Above resistance
                
                # Risk-reward targets
                risk = stop_loss - entry
                target_1 = entry - (risk * 1.5)
                target_2 = entry - (risk * 2.0)
                
                return {
                    'stock': stock,
                    'signal_type': SignalType.SHORT,
                    'entry': round(entry, 2),
                    'stop_loss': round(stop_loss, 2),
                    'target_1': round(target_1, 2),
                    'target_2': round(target_2, 2),
                    'score': score,
                    'reasons': reasons,
                    'sector': sector
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error identifying short setup for {stock}: {e}")
            return None

price_action_strategy = PriceActionStrategy()