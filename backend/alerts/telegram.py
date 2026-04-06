from telegram import Bot
import logging
from config import config
from models import Signal

logger = logging.getLogger(__name__)

class TelegramAlerter:
    """Send trade alerts via Telegram"""
    
    def __init__(self):
        self.bot_token = config.TELEGRAM_BOT_TOKEN
        self.chat_id = config.TELEGRAM_CHAT_ID
        self.bot = None
        
        if self.bot_token:
            try:
                self.bot = Bot(token=self.bot_token)
            except Exception as e:
                logger.error(f"Failed to initialize Telegram bot: {e}")
    
    async def send_signal_alert(self, signal: Signal):
        """Send trading signal alert"""
        if not self.bot or not self.chat_id:
            logger.warning("Telegram not configured. Skipping alert.")
            return False
        
        try:
            message = self._format_signal_message(signal)
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )
            logger.info(f"Telegram alert sent for {signal.stock}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Telegram alert: {e}")
            return False
    
    def _format_signal_message(self, signal: Signal) -> str:
        """Format signal into readable message"""
        emoji = "🟢" if signal.signal_type == "LONG" else "🔴"
        
        message = f"{emoji} *TRADE SIGNAL*\n\n"
        message += f"*STOCK:* {signal.stock}\n"
        message += f"*TYPE:* {signal.signal_type}\n"
        message += f"*ENTRY:* ₹{signal.entry}\n"
        message += f"*STOP LOSS:* ₹{signal.stop_loss}\n"
        message += f"*TARGET 1:* ₹{signal.target_1}\n"
        message += f"*TARGET 2:* ₹{signal.target_2}\n"
        message += f"*POSITION SIZE:* {signal.position_size} qty\n"
        message += f"*CONFIDENCE:* {signal.confidence_score:.1f}/10\n\n"
        
        message += f"*REASONS:*\n"
        for reason in signal.reasons:
            message += f"• {reason}\n"
        
        message += f"\n*Sector:* {signal.sector}\n"
        message += f"*Market:* {signal.market_regime}\n"
        message += f"\n_Generated at {signal.timestamp.strftime('%H:%M:%S')}_"
        
        return message
    
    async def get_chat_id_from_updates(self):
        """Helper to get chat ID from bot updates"""
        if not self.bot:
            return None
        
        try:
            updates = await self.bot.get_updates()
            if updates:
                return updates[-1].message.chat_id
            return None
        except Exception as e:
            logger.error(f"Error getting chat ID: {e}")
            return None

telegram_alerter = TelegramAlerter()