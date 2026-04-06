import logging
from config import config

logger = logging.getLogger(__name__)

class PositionSizer:
    """Calculate risk-based position sizing"""
    
    def __init__(self, capital: float = 500000):
        self.capital = capital
        self.risk_per_trade = config.RISK_PER_TRADE
    
    def calculate_position_size(self, entry: float, stop_loss: float) -> int:
        """Calculate position size based on risk"""
        try:
            if entry <= 0 or stop_loss <= 0:
                return 0
            
            # Calculate risk per share
            risk_per_share = abs(entry - stop_loss)
            
            if risk_per_share == 0:
                return 0
            
            # Calculate position size
            risk_amount = self.capital * self.risk_per_trade
            position_size = int(risk_amount / risk_per_share)
            
            # Ensure minimum viable position
            if position_size < 1:
                position_size = 1
            
            logger.info(f"Position size calculated: {position_size} qty (Capital: {self.capital}, Risk: {risk_amount})")
            return position_size
            
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return 0
    
    def update_capital(self, new_capital: float):
        """Update trading capital"""
        self.capital = new_capital
        logger.info(f"Capital updated to: {new_capital}")

position_sizer = PositionSizer()