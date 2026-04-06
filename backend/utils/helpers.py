from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def format_currency(amount: float) -> str:
    """Format amount as Indian currency"""
    return f"₹{amount:,.2f}"

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change"""
    if old_value == 0:
        return 0
    return ((new_value - old_value) / old_value) * 100

def is_market_hours() -> bool:
    """Check if current time is within market hours (9:15 AM to 3:30 PM IST)"""
    now = datetime.now()
    market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
    market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
    
    # Check if it's a weekday (Monday=0, Sunday=6)
    if now.weekday() >= 5:  # Saturday or Sunday
        return False
    
    return market_open <= now <= market_close

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def get_risk_reward_ratio(entry: float, stop_loss: float, target: float) -> float:
    """Calculate risk-reward ratio"""
    risk = abs(entry - stop_loss)
    reward = abs(target - entry)
    
    if risk == 0:
        return 0
    
    return reward / risk