from typing import Dict, List, Tuple
import logging
from config import config

logger = logging.getLogger(__name__)

class SectorAnalyzer:
    """Analyze sector strength for stock selection"""
    
    def __init__(self):
        self.sector_strength = {}
    
    def analyze_sectors(self, market_data: Dict) -> Dict[str, float]:
        """Calculate strength for each sector"""
        try:
            sector_performance = {}
            
            for sector, stocks in config.SECTORS.items():
                # Calculate average percentage move
                total_change = 0
                valid_stocks = 0
                
                for stock in stocks:
                    if stock in market_data:
                        data = market_data[stock]
                        if data['open'] > 0:
                            pct_change = ((data['close'] - data['open']) / data['open']) * 100
                            total_change += pct_change
                            valid_stocks += 1
                
                if valid_stocks > 0:
                    avg_change = total_change / valid_stocks
                    sector_performance[sector] = avg_change
                else:
                    sector_performance[sector] = 0.0
            
            self.sector_strength = sector_performance
            logger.info(f"Sector analysis complete: {sector_performance}")
            return sector_performance
            
        except Exception as e:
            logger.error(f"Error analyzing sectors: {e}")
            return {}
    
    def get_top_sectors(self, n: int = 2) -> List[str]:
        """Get top N strongest sectors"""
        if not self.sector_strength:
            return []
        
        sorted_sectors = sorted(
            self.sector_strength.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [sector for sector, _ in sorted_sectors[:n]]
    
    def get_weakest_sectors(self, n: int = 2) -> List[str]:
        """Get N weakest sectors"""
        if not self.sector_strength:
            return []
        
        sorted_sectors = sorted(
            self.sector_strength.items(),
            key=lambda x: x[1]
        )
        return [sector for sector, _ in sorted_sectors[:n]]
    
    def get_stock_sector(self, stock: str) -> str:
        """Get sector for a stock"""
        for sector, stocks in config.SECTORS.items():
            if stock in stocks:
                return sector
        return "UNKNOWN"
    
    def is_strong_sector(self, sector: str) -> bool:
        """Check if sector is in top 2 strong"""
        return sector in self.get_top_sectors(2)
    
    def is_weak_sector(self, sector: str) -> bool:
        """Check if sector is in weakest 2"""
        return sector in self.get_weakest_sectors(2)

sector_analyzer = SectorAnalyzer()