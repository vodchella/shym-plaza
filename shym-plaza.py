#!/usr/bin/env python3

import argparse
import os
import sys
from datetime import datetime
from pkg.config import CONFIG
from pkg.connectors.umag import UmagServer
from pkg.constants.date_formats import DATE_FORMAT_FULL, DATE_FORMAT_FILE
from pkg.constants.version import SOFTWARE_VERSION
from pkg.utils.console import panic
from pkg.utils.errors import get_raised_error
from pkg.utils.files import write_file
from pkg.utils.logger import DEFAULT_LOGGER as LOG


def create_argparse():
    parser = argparse.ArgumentParser(description=SOFTWARE_VERSION)
    parser.add_argument(
        '-b',
        '--beg-date',
        required=True,
        help=f'Beginning of period (dd.mm.yyyy hh24:mi:ss)'
    )
    parser.add_argument(
        '-e',
        '--end-date',
        required=True,
        help='End of period (dd.mm.yyyy hh24:mi:ss)'
    )
    return parser.parse_args()


if __name__ == '__main__':
    if sys.version_info < (3, 8):
        panic('We need minimum Python version 3.8 to run. Current version: %s.%s.%s' % sys.version_info[:3])

    args = create_argparse()

    LOG.info(f'{SOFTWARE_VERSION} started')
    with UmagServer() as u:
        LOG.info(f'Server API address: {u}')

        beg_date = datetime.strptime(args.beg_date, DATE_FORMAT_FULL)
        end_date = datetime.strptime(args.end_date, DATE_FORMAT_FULL)
        beg_date_file = beg_date.strftime(DATE_FORMAT_FILE)
        end_date_file = end_date.strftime(DATE_FORMAT_FILE)

        LOG.info(f'Period specified: {args.beg_date} - {args.end_date}\n')

        err_count = 0
        for store in CONFIG['stores']:
            obj_id = store['obj_id']
            store_id = store['id']

            LOG.info(f'Processing store #{store_id} ({obj_id})...')

            try:
                if u.auth(store['login'], store['password']):
                    file_name = f'{obj_id}_{beg_date_file}_{end_date_file}.xml'
                    file_path = os.path.join(CONFIG['output_dir'], file_name)

                    sales = u.get_sales(store_id, obj_id, beg_date, end_date)
                    if sales:
                        write_file(file_path, sales)
                        LOG.info(f'Sales was writen to {file_name}\n')
                else:
                    LOG.error(f'Invalid login or password\n')
                    err_count += 1
            except:
                LOG.error(get_raised_error(True))
                err_count += 1

        LOG.info(f'Processed stores/errors: {len(CONFIG["stores"])}/{err_count}')
