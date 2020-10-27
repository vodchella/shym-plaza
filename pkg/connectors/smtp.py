from pkg.config import CONFIG
from pkg.utils.decorators import singleton


@singleton
class SmtpServer:
    __host = None
    __port = None
    __login = None
    __password = None
    __sender_email = None

    def __init__(self):
        self.__host = CONFIG['smtp']['host']
        self.__port = CONFIG['smtp']['port']
        self.__login = CONFIG['smtp']['login']
        self.__password = CONFIG['smtp']['password']
        self.__sender_email = CONFIG['smtp']['sender_email']

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
