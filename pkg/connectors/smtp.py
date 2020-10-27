import smtplib
import ssl
from pkg.config import CONFIG
from pkg.utils.decorators import singleton
from pkg.utils.errors import get_raised_error
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

    def send_emails(self, subject, text):
        try:
            context = ssl.create_default_context()
            emails_count = len(self.__receivers)
            message = f'Subject: {subject}\n\n{text}'

            SMTP_LOGGER.info('Sending emails...')
            with smtplib.SMTP_SSL(self.__host, self.__port, context=context) as server:
                server.login(self.__login, self.__password)
                for (i, email) in enumerate(self.__receivers, 1):
                    new_line = '\n' if i == emails_count else ''
                    try:
                        server.sendmail(self.__sender, email, message)
                        SMTP_LOGGER.info(f'Email to {email} was successfully sent{new_line}')
                    except:
                        SMTP_LOGGER.error(f'Email to {email} wasn\'t sent{new_line}')
        except:
            SMTP_LOGGER.error(get_raised_error(True))
