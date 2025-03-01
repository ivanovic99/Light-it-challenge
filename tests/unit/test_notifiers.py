import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import BackgroundTasks

from app.services.notifications import NotificationFactory, Notifier
from app.services.email_notifier import EmailNotifier
from app.core.config import settings

class TestNotifier(Notifier):
    """Test notifier implementation for testing factory"""
    async def send_notification(self, recipient, subject, content):
        return True

def test_notification_factory_registration():
    """Test that the factory can register and retrieve notifiers"""
    # Register a test notifier
    NotificationFactory.register_notifier("test", TestNotifier)
    
    # Get the registered notifier
    notifier = NotificationFactory.get_notifier("test")
    
    # Verify correct type
    assert isinstance(notifier, TestNotifier)
    
    # Verify behavior for unregistered type
    with pytest.raises(Exception):
        NotificationFactory.get_notifier("nonexistent")

def test_notification_factory_default_registrations():
    """Test that standard notifiers are registered by default"""
    # Email notifier should be registered
    email_notifier = NotificationFactory.get_notifier("email")
    assert isinstance(email_notifier, EmailNotifier)

@pytest.mark.asyncio
@patch('app.services.email_notifier.SMTP')
async def test_email_notifier_send_notification(mock_smtp):
    """Test email notification sending with mocked SMTP"""
    # Setup mock
    mock_smtp_instance = AsyncMock()
    mock_smtp.return_value.__aenter__.return_value = mock_smtp_instance
    
    # Create notifier and send notification
    notifier = EmailNotifier()
    result = await notifier.send_notification(
        "test@example.com", 
        "Test Subject",
        {"name": "Test User", "message": "Hello world"}
    )
    
    # Verify SMTP was called correctly
    assert result is True
    mock_smtp_instance.send_message.assert_called_once()

@pytest.mark.asyncio
@patch('app.services.email_notifier.SMTP')
async def test_email_notifier_handles_error(mock_smtp):
    """Test error handling in email notification"""
    # Setup mock to raise exception
    mock_smtp_instance = AsyncMock()
    mock_smtp_instance.send_message.side_effect = Exception("SMTP Error")
    mock_smtp.return_value.__aenter__.return_value = mock_smtp_instance
    
    # Create notifier and attempt to send notification
    notifier = EmailNotifier()
    result = await notifier.send_notification(
        "test@example.com", 
        "Test Subject",
        {"name": "Test User", "message": "Hello world"}
    )
    
    # Should return False on error but not raise exception
    assert result is False

def test_notification_scheduling():
    """Test that notifications are properly scheduled as background tasks"""
    # Create mocks
    background_tasks = MagicMock(spec=BackgroundTasks)
    notifier = EmailNotifier()
    
    # Schedule notification
    notifier.schedule_notification(
        background_tasks,
        "test@example.com",
        "Test Subject",
        {"name": "Test User", "message": "Hello world"}
    )
    
    # Verify task was added
    background_tasks.add_task.assert_called_once()
    # First arg should be the send_notification method
    args, _ = background_tasks.add_task.call_args
    assert args[0] == notifier.send_notification
