class NotifierError(Exception):
    """Base error for notification-related issues"""
    pass

class NoNotifierError(NotifierError):
    """Error raised when a requested notifier type is not registered"""
    def __str__(self):
        return "No notifier found for the requested type"
