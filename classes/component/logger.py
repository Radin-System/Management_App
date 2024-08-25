import os
import logging
from ._base import Component, ComponentContainer

LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

LOG_COLORS = {
    'debug': '\033[94m',   # Blue
    'info': '\033[92m',    # Green
    'warning': '\033[93m', # Yellow
    'error': '\033[91m',   # Red
    'critical': '\033[95m' # Magenta
}

LOG_RESET_COLOR = '\033[0m'

class Logger(Component):
    def __init__(self, Name: str) -> None:
        super().__init__(Name)

        self.Process_Type: str = 'Static'
        self.logger = None
        
        self.Setup()

    def Init_Config(self) -> None:
        self.Header          = self.Config.Get('LOG', 'log_header')
        self.Log_File        = self.Config.Get('GLOBALS', 'log_file')
        self.Time_Format     = self.Config.Get('LOG', 'log_time_format')
        self.Debug_Condition = self.Config.Get('GLOBALS', 'debug')

    def Setup(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Create file handler
        file_handler = logging.FileHandler(self.Log_File)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            f'{self.Header[0]} %(asctime)s : %(levelname)s : %(message)s {self.Header[1]}', 
            datefmt=self.Time_Format
        ))

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG if self.Debug_Condition else logging.INFO)
        console_handler.setFormatter(self.ColoredFormatter(self.Header, self.Time_Format))

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        if self.Debug_Condition:
            self.logger.addHandler(console_handler)

    def Check_Folder(self) -> None:
        folder_path = os.path.dirname(self.Log_File)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            self.logger.info(f'Created the log folder and file: {self.Log_File}')

    def log(self, level: str, message: str) -> None:
        level = level.lower()
        if level in LOG_LEVELS:
            log_func = getattr(self.logger, level, None)
            if log_func:
                log_func(message)
            else:
                self.logger.error(f'Logging function not found for level: {level}')
        else:
            self.logger.error(f'Invalid log level: {level}')

    def __call__(self, message: str, level='info') -> None:
        self.log(level, message)

    def Start_Actions(self) -> None:
        self.Check_Folder()

    def Stop_Actions(self) -> None:
        pass

    class ColoredFormatter(logging.Formatter):
        def __init__(self, header, time_format):
            super().__init__(
                f'{header[0]} %(asctime)s : %(levelname)s : %(message)s {header[1]}',
                datefmt=time_format
            )

        def format(self, record):
            log_color = LOG_COLORS.get(record.levelname.lower(), LOG_RESET_COLOR)
            log_message = super().format(record)
            return f'{log_color}{log_message}{LOG_RESET_COLOR}'

    def Loop(self) -> None:
        ...