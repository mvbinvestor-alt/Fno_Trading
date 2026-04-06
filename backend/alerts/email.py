import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from config import config
from models import Signal

logger = logging.getLogger(__name__)

class EmailAlerter:
    """Send trade alerts via email"""
    
    def __init__(self):
        self.sender = config.GMAIL_SENDER
        self.password = config.GMAIL_APP_PASSWORD
        self.recipients = config.EMAIL_RECIPIENTS
    
    async def send_signal_alert(self, signal: Signal):
        """Send trading signal via email"""
        if not self.sender or not self.password:
            logger.warning("Email credentials not configured. Skipping alert.")
            return False
        
        try:
            subject = f"Trade Alert: {signal.signal_type} {signal.stock}"
            html_content = self._format_html_message(signal)
            
            for recipient in self.recipients:
                if recipient:
                    await self._send_email(recipient, subject, html_content)
            
            logger.info(f"Email alert sent for {signal.stock}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            return False
    
    async def _send_email(self, to_email: str, subject: str, html_content: str):
        """Send individual email"""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = to_email
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        try:
            await aiosmtplib.send(
                msg,
                hostname='smtp.gmail.com',
                port=587,
                start_tls=True,
                username=self.sender,
                password=self.password
            )
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {e}")
            raise
    
    def _format_html_message(self, signal: Signal) -> str:
        """Format signal into HTML email"""
        color = "#10B981" if signal.signal_type == "LONG" else "#EF4444"
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: {color}; color: white; padding: 20px; text-align: center; }}
                .content {{ background-color: #f9f9f9; padding: 20px; }}
                .signal-detail {{ margin: 10px 0; padding: 10px; background: white; border-left: 4px solid {color}; }}
                .label {{ font-weight: bold; color: #666; }}
                .value {{ color: #000; font-size: 18px; }}
                .reasons {{ background: white; padding: 15px; margin-top: 20px; }}
                .reasons li {{ margin: 5px 0; }}
                .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>TRADE SIGNAL</h1>
                    <h2>{signal.stock} - {signal.signal_type}</h2>
                </div>
                <div class="content">
                    <div class="signal-detail">
                        <span class="label">ENTRY:</span> 
                        <span class="value">₹{signal.entry}</span>
                    </div>
                    <div class="signal-detail">
                        <span class="label">STOP LOSS:</span> 
                        <span class="value">₹{signal.stop_loss}</span>
                    </div>
                    <div class="signal-detail">
                        <span class="label">TARGET 1:</span> 
                        <span class="value">₹{signal.target_1}</span>
                    </div>
                    <div class="signal-detail">
                        <span class="label">TARGET 2:</span> 
                        <span class="value">₹{signal.target_2}</span>
                    </div>
                    <div class="signal-detail">
                        <span class="label">POSITION SIZE:</span> 
                        <span class="value">{signal.position_size} qty</span>
                    </div>
                    <div class="signal-detail">
                        <span class="label">CONFIDENCE:</span> 
                        <span class="value">{signal.confidence_score:.1f}/10</span>
                    </div>
                    
                    <div class="reasons">
                        <h3>REASONS:</h3>
                        <ul>
        """
        
        for reason in signal.reasons:
            html += f"<li>{reason}</li>\n"
        
        html += f"""
                        </ul>
                    </div>
                    
                    <div class="signal-detail">
                        <span class="label">Sector:</span> {signal.sector}<br>
                        <span class="label">Market Regime:</span> {signal.market_regime}
                    </div>
                </div>
                <div class="footer">
                    <p>Generated at {signal.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>F&O Trading System - Automated Alert</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html

email_alerter = EmailAlerter()