from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from signal_generator import SignalGenerator
from utils.helpers import is_market_hours

logger = logging.getLogger(__name__)

class TradingScheduler:
    """Schedule automated signal generation"""
    
    def __init__(self, signal_generator: SignalGenerator):
        self.scheduler = AsyncIOScheduler()
        self.signal_generator = signal_generator
        self.is_running = False
    
    def start(self):
        """Start the scheduler"""
        if self.is_running:
            logger.warning("Scheduler already running")
            return
        
        # Run every 5 minutes during market hours (9:15 AM to 3:30 PM, Mon-Fri)
        self.scheduler.add_job(
            self._scheduled_signal_generation,
            CronTrigger(
                day_of_week='mon-fri',
                hour='9-15',
                minute='*/5'
            ),
            id='signal_generation',
            name='Generate Trading Signals',
            replace_existing=True
        )
        
        self.scheduler.start()
        self.is_running = True
        logger.info("Trading scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        if not self.is_running:
            return
        
        self.scheduler.shutdown()
        self.is_running = False
        logger.info("Trading scheduler stopped")
    
    async def _scheduled_signal_generation(self):
        """Scheduled task for signal generation"""
        try:
            # Double-check market hours
            if not is_market_hours():
                logger.info("Outside market hours. Skipping signal generation.")
                return
            
            logger.info("Running scheduled signal generation...")
            signals = await self.signal_generator.generate_signals()
            logger.info(f"Scheduled run completed. Generated {len(signals)} signals.")
            
        except Exception as e:
            logger.error(f"Scheduled signal generation error: {e}")
    
    def get_status(self) -> dict:
        """Get scheduler status"""
        return {
            'is_running': self.is_running,
            'jobs': [{
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time.isoformat() if job.next_run_time else None
            } for job in self.scheduler.get_jobs()]
        }