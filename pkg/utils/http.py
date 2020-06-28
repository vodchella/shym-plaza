from pkg.constants.version import SOFTWARE_VERSION
from requests import Session, request as req


def request(method: str, url: str, **kwargs):
    session = Session()
    headers = {
        'User-Agent': f'{SOFTWARE_VERSION} ({session.headers["User-Agent"]})'
    }
    return req(method, url, headers=headers, **kwargs)
