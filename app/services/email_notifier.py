import logging
from typing import Dict, Any

from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.services.notifications import Notifier, NotificationFactory
from app.core.config import settings

logger = logging.getLogger(__name__)

class EmailNotifier(Notifier):
    """Email notification implementation"""
    
    async def send_notification(self, recipient: str, subject: str, content: Dict[str, Any]) -> bool:
        """Send email notification"""
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = settings.EMAIL_USER
            message["To"] = recipient
            
            html = f"""
            <html>
            <body>
                <h2>{subject}</h2>
                <p>Dear {content.get('name', 'Patient')},</p>
                <p>{content.get('message', 'Thank you for registering with our service.')}</p>
                <p>Best regards,<br>Patient Registration Team</p>
            </body>
            </html>
            """
            
            message.attach(MIMEText(html, "html"))
            
            async with SMTP(
                hostname=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_USER,
                password=settings.EMAIL_PASSWORD,
                use_tls=False,  # Start with plain connection
                start_tls=True,  # Auto-upgrade to TLS
            ) as smtp:
                await smtp.send_message(message)
                
            logger.info(f"Email notification sent to {recipient}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email notification: {str(e)}")
            return False

NotificationFactory.register_notifier("email", EmailNotifier)
