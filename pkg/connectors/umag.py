import base64
from datetime import datetime
from json.decoder import JSONDecodeError
from pkg.constants.date_formats import DATE_FORMAT_UMAG
from pkg.utils.console import panic
from pkg.utils.decorators import singleton
from pkg.utils.http import request

UMAG_BASIC_HEADERS = {
    'api-ver': '0.9',
    'client-ver': '1c_integrator_0.0.1',
}


@singleton
class UmagServer:
    __base_url = None
    __access_token = None

    def __init__(self):
        addr = 'localhost'
        port = 8080
        self.__base_url = f'http://{addr}:{port}/rest/'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def auth(self, login: str, password: str):
        encoded_credentials = base64.standard_b64encode(f'{login}:{password}'.encode('utf-8'))
        headers = {
            **UMAG_BASIC_HEADERS,
            'Authorization': f'Basic {str(encoded_credentials, "utf-8")}',
        }
        response = request('GET', self.__base_url + 'cabinet/org/auth/authenticate', headers)

        try:
            resp_json = response.json()
            token = resp_json['properties']['access_token']
            self.__access_token = token
            return token
        except JSONDecodeError:
            panic(f'Invalid login or password: {login} {password}')

    def get_sales(self, store_id: int, object_id: str, beg_date: datetime, end_date: datetime):
        headers = {
            **UMAG_BASIC_HEADERS,
            'Authorization': self.__access_token,
        }
        querystring = {
            'storeId': store_id,
            'objectId': object_id,
            'begDate': beg_date.strftime(DATE_FORMAT_UMAG),
            'endDate': end_date.strftime(DATE_FORMAT_UMAG),
        }
        return request('GET', self.__base_url + 'integration/shym-plaza/sales.xml', headers, params=querystring).text
