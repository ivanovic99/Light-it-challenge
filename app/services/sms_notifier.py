import logging
from typing import Dict, Any

from app.services.notifications import Notifier, NotificationFactory

logger = logging.getLogger(__name__)

class SMSNotifier(Notifier):
    """SMS notification implementation (placeholder)"""
    
    async def send_notification(self, recipient: str, subject: str, content: Dict[str, Any]) -> bool:
        """Send SMS notification"""
        try:
            logger.info(f"SMS notification would be sent to {recipient}: {subject}")
            return True
        except Exception as e:
            logger.error(f"Failed to send SMS notification: {str(e)}")
            return False

NotificationFactory.register_notifier("sms", SMSNotifier)
