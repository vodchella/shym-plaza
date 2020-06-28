import sys
from datetime import datetime
from pkg.connectors.umag import UmagServer
from pkg.constants.date_formats import DATE_FORMAT_FULL
from pkg.utils.console import panic

if __name__ == '__main__':
    if sys.version_info < (3, 8):
        panic('We need minimum Python version 3.8 to run. Current version: %s.%s.%s' % sys.version_info[:3])

    with UmagServer() as u:
        u.auth('+77761522222', '11111')
        beg_date = datetime.strptime('28.06.2020 00:00:00', DATE_FORMAT_FULL)
        end_date = datetime.strptime('28.06.2020 23:59:59', DATE_FORMAT_FULL)
        print(u.get_sales(1, '0x123456789', beg_date, end_date))

