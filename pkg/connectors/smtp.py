from pkg.config import CONFIG
from pkg.utils.decorators import singleton
from pkg.utils.logger import SMTP_LOGGER


@singleton
class SmtpServer:
    __initialized = False
    __host = None
    __port = None
    __login = None
    __password = None
    __sender = None
    __receivers = []

    def __init__(self):
        try:
            self.__host = CONFIG['smtp']['host']
            self.__port = CONFIG['smtp']['port']
            self.__login = CONFIG['smtp']['login']
            self.__password = CONFIG['smtp']['password']
            self.__sender = CONFIG['smtp']['sender']
            self.__receivers = CONFIG['smtp']['receivers']
            self.__initialized = True
        except KeyError:
            SMTP_LOGGER.error('Can\'t initialize smtp connector\n')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def is_initialized(self):
        return self.__initialized

    def send_emails(self):
        emails_count = len(self.__receivers)
        for (i, email) in enumerate(self.__receivers, 1):
            new_line = '\n' if i == emails_count else ''
            SMTP_LOGGER.info(f'Sending notify to {email}{new_line}')
