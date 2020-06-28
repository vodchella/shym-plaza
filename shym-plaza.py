import os
import sys
from datetime import datetime
from pkg.config import CONFIG
from pkg.connectors.umag import UmagServer
from pkg.constants.date_formats import DATE_FORMAT_FULL, DATE_FORMAT_FILE
from pkg.utils.console import panic
from pkg.utils.files import write_file

if __name__ == '__main__':
    if sys.version_info < (3, 8):
        panic('We need minimum Python version 3.8 to run. Current version: %s.%s.%s' % sys.version_info[:3])

    with UmagServer() as u:
        for store in CONFIG['stores']:
            beg_date_str = '28.06.2020 00:00:00'
            end_date_str = '28.06.2020 23:59:59'
            beg_date = datetime.strptime(beg_date_str, DATE_FORMAT_FULL)
            end_date = datetime.strptime(end_date_str, DATE_FORMAT_FULL)
            obj_id = store['obj_id']

            u.auth(store['login'], store['password'])
            sales = u.get_sales(1, obj_id, beg_date, end_date)

            beg_date_file = beg_date.strftime(DATE_FORMAT_FILE)
            end_date_file = end_date.strftime(DATE_FORMAT_FILE)
            file_name = f'{obj_id}_{beg_date_file}_{end_date_file}.xml'
            file_path = os.path.join(CONFIG['output_dir'], file_name)

            write_file(file_path, sales)

