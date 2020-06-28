import sys
from pkg.connectors.umag import UmagServer
from pkg.utils.console import panic

if __name__ == '__main__':
    if sys.version_info < (3, 8):
        panic('We need minimum Python version 3.8 to run. Current version: %s.%s.%s' % sys.version_info[:3])

    print(UmagServer().auth('+77761522222', '11111'))

