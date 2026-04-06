from typing import Dict
import logging
from models import MarketRegime, SignalType

logger = logging.getLogger(__name__)

class SignalScorer:
    """Score trading signals based on multiple factors"""
    
    WEIGHTS = {
        'price_action': 3,
        'volume': 2,
        'option_chain': 3,
        'sector_strength': 2,
        'regime_alignment': 2,
        'news_sentiment': 1
    }
    
    def calculate_score(self, setup: Dict, regime: MarketRegime, 
                       sector_strong: bool, sector_weak: bool,
                       option_score: int, sentiment_score: int = 0) -> Dict:
        """Calculate comprehensive signal score"""
        try:
            total_score = 0
            score_breakdown = {}
            
            # Price action score (already calculated)
            price_score = setup.get('score', 0)
            total_score += price_score
            score_breakdown['price_action'] = price_score
            
            # Volume score
            volume_score = 2  # Already checked in price action
            total_score += volume_score
            score_breakdown['volume'] = volume_score
            
            # Option chain score
            oc_score = max(0, option_score)  # Option score from analyzer
            total_score += oc_score
            score_breakdown['option_chain'] = oc_score
            
            # Sector strength score
            signal_type = setup['signal_type']
            if signal_type == SignalType.LONG and sector_strong:
                sect_score = 2
            elif signal_type == SignalType.SHORT and sector_weak:
                sect_score = 2
            else:
                sect_score = 0
            
            total_score += sect_score
            score_breakdown['sector_strength'] = sect_score
            
            # Regime alignment score
            regime_score = 2  # Already checked in strategy
            total_score += regime_score
            score_breakdown['regime_alignment'] = regime_score
            
            # News sentiment score
            total_score += sentiment_score
            score_breakdown['news_sentiment'] = sentiment_score
            
            return {
                'total_score': total_score,
                'breakdown': score_breakdown,
                'confidence': min(10, total_score / 1.3)  # Normalize to 0-10
            }
            
        except Exception as e:
            logger.error(f"Error calculating score: {e}")
            return {
                'total_score': 0,
                'breakdown': {},
                'confidence': 0
            }

signal_scorer = SignalScorer()