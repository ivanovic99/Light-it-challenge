import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Type

from fastapi import BackgroundTasks

from app.errors.notifier import NoNotifierError

logger = logging.getLogger(__name__)

class Notifier(ABC):
    """Abstract base class for all notification services"""
    
    @abstractmethod
    async def send_notification(self, recipient: str, subject: str, content: Dict[str, Any]) -> bool:
        """Send notification to recipient with given content"""
        pass
    
    def schedule_notification(self, background_tasks: BackgroundTasks, recipient: str, 
                             subject: str, content: Dict[str, Any]) -> None:
        """Schedule notification to be sent in background"""
        background_tasks.add_task(self.send_notification, recipient, subject, content)


class NotificationFactory:
    """Factory for creating notifiers"""
    _notifiers = {}
    
    @classmethod
    def register_notifier(cls, name: str, notifier_class: Type[Notifier]):
        """Register a notifier class with the factory"""
        cls._notifiers[name.lower()] = notifier_class
        
    @classmethod
    def get_notifier(cls, type: str = "email") -> Notifier:
        """Get appropriate notifier based on type"""
        notifier_class = cls._notifiers.get(type.lower())
        if not notifier_class:
            raise NoNotifierError()
        return notifier_class()
