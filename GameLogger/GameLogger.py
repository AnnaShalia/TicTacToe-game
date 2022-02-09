import logging
from FileOperator.FileOperator import FileOperator


class GameLogger:

    """
    Creates a logger handler
    and allows operations with log file.
    """

    # init logger handler, set format for the message to be recorded in the file
    def __init__(self, file_handler_path='stats.log'):
        self.file_path = file_handler_path
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        logger_handler = logging.FileHandler(self.file_path)
        logger_handler.setLevel(logging.INFO)
        logger_handler.setFormatter(logging.Formatter(fmt='%(asctime)s - %(message)s',
                                                      datefmt='%d.%m.%y %H:%M'))
        self.logger.addHandler(logger_handler)

    def clean_logs(self):
        with FileOperator(self.file_path, 'r+') as file:
            file.truncate(0)

    def add_log_msg(self, message):
        self.logger.info(message)

    def show_logs(self):
        with FileOperator(self.file_path, 'r') as file:
            print(file.read())
