from pkg.constants.version import SOFTWARE_VERSION
from requests import Session, request as req


def request(method: str, url: str, headers: dict, **kwargs):
    session = Session()
    hdr = {
        **headers,
        'User-Agent': f'{SOFTWARE_VERSION} ({session.headers["User-Agent"]})'
    }
    return req(method, url, headers=hdr, **kwargs)
