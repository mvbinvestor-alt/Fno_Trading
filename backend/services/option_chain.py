from typing import Dict
import logging

logger = logging.getLogger(__name__)

class OptionChainAnalyzer:
    """Analyze option chain data for trading signals"""
    
    def analyze_option_chain(self, option_data: Dict) -> Dict:
        """Analyze option chain and return signal"""
        try:
            call_oi = option_data.get('call_oi', 0)
            put_oi = option_data.get('put_oi', 0)
            call_oi_change = option_data.get('call_oi_change', 0)
            put_oi_change = option_data.get('put_oi_change', 0)
            pcr = option_data.get('pcr', 1.0)
            
            score = 0
            signal = "NEUTRAL"
            reasons = []
            
            # Bullish signals
            if put_oi_change > 0 and put_oi_change > abs(call_oi_change) * 1.5:
                score += 1
                reasons.append("Put OI buildup")
            
            if pcr > 1.0:
                score += 1
                reasons.append(f"PCR bullish: {pcr:.2f}")
            
            if call_oi_change < 0:
                score += 1
                reasons.append("Call OI unwinding")
            
            # Bearish signals
            if call_oi_change > 0 and call_oi_change > abs(put_oi_change) * 1.5:
                score -= 1
                reasons.append("Call OI buildup")
            
            if pcr < 0.8:
                score -= 1
                reasons.append(f"PCR bearish: {pcr:.2f}")
            
            if put_oi_change < 0:
                score -= 1
                reasons.append("Put OI unwinding")
            
            # Determine signal
            if score >= 2:
                signal = "BULLISH"
            elif score <= -2:
                signal = "BEARISH"
            
            return {
                'signal': signal,
                'score': score,
                'reasons': reasons,
                'pcr': pcr
            }
            
        except Exception as e:
            logger.error(f"Error analyzing option chain: {e}")
            return {
                'signal': 'NEUTRAL',
                'score': 0,
                'reasons': [],
                'pcr': 1.0
            }

option_analyzer = OptionChainAnalyzer()
