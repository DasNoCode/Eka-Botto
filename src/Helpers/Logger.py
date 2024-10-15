import logging
from datetime import datetime


class CustomFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[92m",
        "INFO": "\033[94m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "NOTICE": "\033[95m",
        "RESET": "\033[0m",
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"{log_color}{log_time} - {record.levelname} - {record.getMessage()}{self.COLORS['RESET']}"
        return formatted_message


NOTICE_LEVEL_NUM = 25
logging.addLevelName(NOTICE_LEVEL_NUM, "NOTICE")


def notice(self, message, *args, **kws):
    if self.isEnabledFor(NOTICE_LEVEL_NUM):
        self._log(NOTICE_LEVEL_NUM, message, args, **kws)


logging.Logger.notice = notice


def get_logger():
    logger = logging.getLogger("custom_logger")
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = CustomFormatter()
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger
