import logging
import sys

class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log levels"""
    
    COLORS = {
        'DEBUG': '\033[92m',     # Green
        'INFO': '\033[94m',      # Blue
        'WARNING': '\033[93m',   # Yellow
        'ERROR': '\033[91m',     # Red
        'CRITICAL': '\033[91;1m', # Bold Red
        'RESET': '\033[0m'       # Reset to default
    }
    
    def format(self, record):
        levelname = record.levelname
        
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        message = super().format(record)
        
        record.levelname = levelname
        
        return message

def setup_logging(log_level=logging.INFO):
    """Configure application logging with colored output"""
    formatter = ColoredFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers = [handler]

    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.DEBUG)
    
    return root_logger
