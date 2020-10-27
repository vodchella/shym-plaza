import logging.config
import logging.handlers
from pkg.config.logger import LOG_CONFIG
from pkg.constants.logger import *


logging.config.dictConfig(LOG_CONFIG)

DEFAULT_LOGGER = logging.getLogger(DEFAULT_LOGGER_NAME)
FTP_LOGGER = logging.getLogger(FTP_LOGGER_NAME)
SMTP_LOGGER = logging.getLogger(SMTP_LOGGER_NAME)
UMAG_LOGGER = logging.getLogger(UMAG_LOGGER_NAME)
