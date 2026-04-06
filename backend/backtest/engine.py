from typing import List, Dict
from datetime import datetime, timedelta
import logging
from models import Signal, Trade
import numpy as np

logger = logging.getLogger(__name__)

class BacktestEngine:
    """Backtesting engine for strategy validation"""
    
    def __init__(self):
        self.trades = []
        self.equity_curve = []
        self.initial_capital = 500000
        self.capital = self.initial_capital
    
    def run_backtest(self, signals: List[Signal], historical_data: Dict) -> Dict:
        """Run backtest on historical signals"""
        try:
            self.trades = []
            self.equity_curve = []
            self.capital = self.initial_capital
            
            for signal in signals:
                trade_result = self._simulate_trade(signal, historical_data)
                if trade_result:
                    self.trades.append(trade_result)
                    self.capital += trade_result['pnl']
                    self.equity_curve.append({
                        'timestamp': trade_result['exit_time'],
                        'capital': self.capital
                    })
            
            metrics = self._calculate_metrics()
            
            return {
                'trades': self.trades,
                'equity_curve': self.equity_curve,
                'metrics': metrics,
                'total_trades': len(self.trades),
                'initial_capital': self.initial_capital,
                'final_capital': self.capital
            }
            
        except Exception as e:
            logger.error(f"Backtest error: {e}")
            return {}
    
    def _simulate_trade(self, signal: Signal, historical_data: Dict) -> Dict:
        """Simulate a single trade"""
        try:
            # Simplified simulation - in production, use actual tick data
            entry = signal.entry
            stop_loss = signal.stop_loss
            target_1 = signal.target_1
            target_2 = signal.target_2
            position_size = signal.position_size
            
            # Simulate outcome (random for demo - use real data in production)
            import random
            outcome = random.choice(['target_1', 'target_2', 'stop_loss'])
            
            if outcome == 'target_1':
                exit_price = target_1
            elif outcome == 'target_2':
                exit_price = target_2
            else:
                exit_price = stop_loss
            
            # Calculate P&L
            if signal.signal_type == "LONG":
                pnl = (exit_price - entry) * position_size
            else:
                pnl = (entry - exit_price) * position_size
            
            return {
                'signal_id': signal.id,
                'stock': signal.stock,
                'signal_type': signal.signal_type,
                'entry_price': entry,
                'exit_price': exit_price,
                'position_size': position_size,
                'entry_time': signal.timestamp,
                'exit_time': signal.timestamp + timedelta(hours=2),
                'pnl': round(pnl, 2),
                'outcome': outcome
            }
            
        except Exception as e:
            logger.error(f"Trade simulation error: {e}")
            return None
    
    def _calculate_metrics(self) -> Dict:
        """Calculate performance metrics"""
        try:
            if not self.trades:
                return {}
            
            # Win rate
            winning_trades = [t for t in self.trades if t['pnl'] > 0]
            win_rate = (len(winning_trades) / len(self.trades)) * 100
            
            # Average P&L
            avg_win = np.mean([t['pnl'] for t in winning_trades]) if winning_trades else 0
            losing_trades = [t for t in self.trades if t['pnl'] <= 0]
            avg_loss = np.mean([t['pnl'] for t in losing_trades]) if losing_trades else 0
            
            # Risk-Reward Ratio
            avg_rr = abs(avg_win / avg_loss) if avg_loss != 0 else 0
            
            # Max Drawdown
            equity_values = [e['capital'] for e in self.equity_curve]
            max_dd = self._calculate_max_drawdown(equity_values)
            
            # Total Return
            total_return = ((self.capital - self.initial_capital) / self.initial_capital) * 100
            
            return {
                'win_rate': round(win_rate, 2),
                'avg_win': round(avg_win, 2),
                'avg_loss': round(avg_loss, 2),
                'avg_rr': round(avg_rr, 2),
                'max_drawdown': round(max_dd, 2),
                'total_return': round(total_return, 2),
                'total_trades': len(self.trades),
                'winning_trades': len(winning_trades),
                'losing_trades': len(losing_trades)
            }
            
        except Exception as e:
            logger.error(f"Metrics calculation error: {e}")
            return {}
    
    def _calculate_max_drawdown(self, equity_values: List[float]) -> float:
        """Calculate maximum drawdown"""
        if not equity_values:
            return 0
        
        peak = equity_values[0]
        max_dd = 0
        
        for value in equity_values:
            if value > peak:
                peak = value
            dd = ((peak - value) / peak) * 100
            if dd > max_dd:
                max_dd = dd
        
        return max_dd

backtest_engine = BacktestEngine()