import logging
import sys
import re


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629
    and https://alexandra-zaharia.github.io/posts/make-your-own-custom-color-formatter-with-python-logging/
    """

    grey = "\x1b[38;21m"
    green = "\x1b[38;5;42m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.SUCCESS: self.green + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class RedirectStreamToLogger:
    """
    Fake file-like stream object that redirects writes to a logger instance.
    Ref: https://stackoverflow.com/questions/19425736/how-to-redirect-stdout-and-stderr-to-logger-in-python/39215961#39215961
    """

    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.linebuf = ""

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            # Here we redirect this certain string to logging.INFO, since there's no actual error written to stderr while downloading:
            if re.search("Downloading", line) or line == "":
                self.logger.log(logging.INFO, line.rstrip())
                continue
            self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass


def add_logging_level_success():
    """
    A dirty hack to add a custom logging level called 'success'.
    Ref: https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility/13638084#13638084
    """
    logging.SUCCESS = logging.DEBUG + 5  # = 15
    logging.addLevelName(logging.SUCCESS, "SUCCESS")

    def success(self, message, *args, **kws):
        if self.isEnabledFor(logging.SUCCESS):
            self._log(logging.SUCCESS, message, args, **kws)

    logging.Logger.success = success


add_logging_level_success()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Log to console
ch = logging.StreamHandler()
ch.setLevel(logging.SUCCESS)
ch.setFormatter(
    CustomFormatter(
        "%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )
)

logger.addHandler(ch)

sys.stdout = RedirectStreamToLogger(logger, logging.INFO)
sys.stderr = RedirectStreamToLogger(logger, logging.ERROR)
