import logging
from typing import List
from datetime import datetime
from services.market_data import market_data_client
from services.regime_detection import regime_detector
from services.sector_strength import sector_analyzer
from services.option_chain import option_analyzer
from services.price_action import price_action_strategy
from services.scoring import signal_scorer
from services.position_sizing import position_sizer
from alerts import telegram_alerter, email_alerter
from models import Signal, MarketRegime
from config import config
from motor.motor_asyncio import AsyncIOMotorClient
import os

logger = logging.getLogger(__name__)

class SignalGenerator:
    """Main signal generation orchestrator"""
    
    def __init__(self, db):
        self.db = db
        self.active_signals = []
    
    async def generate_signals(self) -> List[Signal]:
        """Main signal generation pipeline"""
        try:
            logger.info("Starting signal generation...")
            
            # Step 1: Get all F&O stocks (simplified - top 30 for demo)
            all_stocks = []
            for sector, stocks in config.SECTORS.items():
                all_stocks.extend(stocks)
            
            # Step 2: Get market data
            logger.info("Fetching market data...")
            market_data = await market_data_client.get_market_data(all_stocks)
            nifty_data = await market_data_client.get_nifty_data()
            
            if not market_data or 'NIFTY' not in nifty_data:
                logger.error("Failed to fetch market data")
                return []
            
            nifty_info = nifty_data['NIFTY']
            
            # Step 3: Detect market regime
            logger.info("Detecting market regime...")
            market_breadth = {'ad_ratio': 1.1}  # Simplified
            regime = regime_detector.detect_regime(nifty_info, market_breadth)
            logger.info(f"Market regime: {regime}")
            
            # Skip if sideways market
            if regime == MarketRegime.SIDEWAYS:
                logger.info("Market is sideways. Skipping signal generation.")
                return []
            
            # Step 4: Analyze sectors
            logger.info("Analyzing sectors...")
            sector_analyzer.analyze_sectors(market_data)
            
            # Step 5: Generate signals for each stock
            signals = []
            
            for stock, data in market_data.items():
                try:
                    # Get sector
                    sector = sector_analyzer.get_stock_sector(stock)
                    
                    # Filter by sector strength
                    if regime == MarketRegime.BULLISH:
                        if not sector_analyzer.is_strong_sector(sector):
                            continue
                    elif regime == MarketRegime.BEARISH:
                        if not sector_analyzer.is_weak_sector(sector):
                            continue
                    
                    # Get option chain data
                    option_data = await market_data_client.get_option_chain(stock)
                    option_analysis = option_analyzer.analyze_option_chain(option_data)
                    
                    # Identify setup
                    setup = None
                    if regime == MarketRegime.BULLISH:
                        setup = price_action_strategy.identify_long_setup(
                            stock, data, regime, sector, option_analysis['signal']
                        )
                    elif regime == MarketRegime.BEARISH:
                        setup = price_action_strategy.identify_short_setup(
                            stock, data, regime, sector, option_analysis['signal']
                        )
                    
                    if not setup:
                        continue
                    
                    # Calculate score
                    score_result = signal_scorer.calculate_score(
                        setup, regime,
                        sector_analyzer.is_strong_sector(sector),
                        sector_analyzer.is_weak_sector(sector),
                        option_analysis['score']
                    )
                    
                    total_score = score_result['total_score']
                    
                    # Check minimum score threshold
                    if total_score < config.MIN_SIGNAL_SCORE:
                        continue
                    
                    # Calculate position size
                    position_size = position_sizer.calculate_position_size(
                        setup['entry'], setup['stop_loss']
                    )
                    
                    if position_size == 0:
                        continue
                    
                    # Create signal
                    signal = Signal(
                        stock=setup['stock'],
                        signal_type=setup['signal_type'],
                        entry=setup['entry'],
                        stop_loss=setup['stop_loss'],
                        target_1=setup['target_1'],
                        target_2=setup['target_2'],
                        position_size=position_size,
                        confidence_score=score_result['confidence'],
                        reasons=setup['reasons'] + [f"Total score: {total_score}"],
                        sector=sector,
                        market_regime=regime
                    )
                    
                    signals.append(signal)
                    logger.info(f"Signal generated for {stock}: {setup['signal_type']}")
                    
                except Exception as e:
                    logger.error(f"Error processing {stock}: {e}")
                    continue
            
            # Limit to max concurrent trades
            signals = signals[:config.MAX_CONCURRENT_TRADES]
            
            # Save signals to database
            for signal in signals:
                await self._save_signal(signal)
            
            # Send alerts
            for signal in signals:
                await self._send_alerts(signal)
            
            logger.info(f"Generated {len(signals)} signals")
            return signals
            
        except Exception as e:
            logger.error(f"Signal generation error: {e}")
            return []
    
    async def _save_signal(self, signal: Signal):
        """Save signal to database"""
        try:
            signal_dict = signal.model_dump()
            signal_dict['timestamp'] = signal_dict['timestamp'].isoformat()
            await self.db.signals.insert_one(signal_dict)
        except Exception as e:
            logger.error(f"Error saving signal: {e}")
    
    async def _send_alerts(self, signal: Signal):
        """Send signal alerts"""
        try:
            # Telegram alert
            await telegram_alerter.send_signal_alert(signal)
            
            # Email alert
            await email_alerter.send_signal_alert(signal)
            
        except Exception as e:
            logger.error(f"Error sending alerts: {e}")