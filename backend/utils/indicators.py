import talib
import numpy as np

def calculate_vwap(prices: np.ndarray, volumes: np.ndarray) -> float:
    """Calculate VWAP (Volume Weighted Average Price)"""
    if len(prices) != len(volumes) or len(prices) == 0:
        return 0
    
    return np.sum(prices * volumes) / np.sum(volumes)

def calculate_rsi(prices: np.ndarray, period: int = 14) -> float:
    """Calculate RSI"""
    try:
        rsi = talib.RSI(prices, timeperiod=period)
        return rsi[-1] if len(rsi) > 0 else 50
    except:
        return 50

def calculate_ema(prices: np.ndarray, period: int = 20) -> float:
    """Calculate EMA"""
    try:
        ema = talib.EMA(prices, timeperiod=period)
        return ema[-1] if len(ema) > 0 else prices[-1]
    except:
        return prices[-1] if len(prices) > 0 else 0

def is_bullish_engulfing(open_prev: float, close_prev: float, 
                         open_curr: float, close_curr: float) -> bool:
    """Check for bullish engulfing pattern"""
    return (close_prev < open_prev and  # Previous candle bearish
            close_curr > open_curr and  # Current candle bullish
            open_curr < close_prev and  # Opens below previous close
            close_curr > open_prev)     # Closes above previous open

def is_bearish_engulfing(open_prev: float, close_prev: float,
                         open_curr: float, close_curr: float) -> bool:
    """Check for bearish engulfing pattern"""
    return (close_prev > open_prev and  # Previous candle bullish
            close_curr < open_curr and  # Current candle bearish
            open_curr > close_prev and  # Opens above previous close
            close_curr < open_prev)     # Closes below previous open