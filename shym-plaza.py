#!/usr/bin/env python3

import os
import sys
from datetime import datetime
from ftplib import FTP
from pkg.arg_parser import create_argparse
from pkg.config import CONFIG, CFG_FILE
from pkg.connectors.umag import UmagServer
from pkg.constants.date_formats import DATE_FORMAT_FULL, DATE_FORMAT_FILE
from pkg.constants.version import SOFTWARE_VERSION, APP_NAME
from pkg.utils.console import panic
from pkg.utils.errors import get_raised_error
from pkg.utils.files import write_file
from pkg.utils.logger import DEFAULT_LOGGER, FTP_LOGGER, UMAG_LOGGER


def download_sales(beg_date: datetime, end_date: datetime):
    with UmagServer() as umag:
        UMAG_LOGGER.info(f'Getting sales from UMAG {umag}...')

        beg_date_file = beg_date.strftime(DATE_FORMAT_FILE)
        end_date_file = end_date.strftime(DATE_FORMAT_FILE)

        UMAG_LOGGER.info(f'Period specified: {args.beg_date} - {args.end_date}\n')

        err_count = 0
        for store in CONFIG['stores']:
            obj_id = store['obj_id']
            store_id = store['id']

            UMAG_LOGGER.info(f'Processing store #{store_id} ({obj_id})...')

            try:
                if umag.auth(store['login'], store['password']):
                    file_name = f'{obj_id}_{beg_date_file}_{end_date_file}.xml'
                    file_path = os.path.join(CONFIG['output_dir'], file_name)

                    sales = umag.get_sales(store_id, obj_id, beg_date, end_date)
                    if sales:
                        write_file(file_path, sales)
                        UMAG_LOGGER.info(f'Sales was writen to {file_name}\n')
                    else:
                        err_count += 1
                else:
                    UMAG_LOGGER.error(f'Invalid login or password\n')
                    err_count += 1
            except:
                UMAG_LOGGER.error(get_raised_error(True))
                err_count += 1

        UMAG_LOGGER.info(f'Processed stores/errors: {len(CONFIG["stores"])}/{err_count}\n')


def upload_files(delete_uploaded_files: bool):
    ftp_host = CONFIG['ftp']['host']
    ftp_port = int(CONFIG['ftp']['port'])
    ftp_login = CONFIG['ftp']['login']
    ftp_password = CONFIG['ftp']['password']
    ftp_upload_dir = CONFIG['ftp']['upload_dir']
    FTP_LOGGER.info(f'Connecting to ftp://{ftp_login}@{ftp_host}:{ftp_port}...')

    ftp_connected = False
    ftp = FTP()
    try:
        ftp.connect(ftp_host, ftp_port)
        ftp_connected = True
        FTP_LOGGER.info(ftp.login(ftp_login, ftp_password))
        ftp.cwd(ftp_upload_dir)

        files_cnt = 0
        for file_name in os.listdir(CONFIG['output_dir']):
            if file_name[-4:] == '.xml':
                file_path = os.path.join(CONFIG['output_dir'], file_name)
                with open(file_path, 'rb') as fobj:
                    FTP_LOGGER.info(f'Uploading file {file_name}...')
                    ftp.storbinary('STOR ' + file_name, fobj, 1024)
                    files_cnt += 1

                    if delete_uploaded_files:
                        os.remove(file_path)
                        FTP_LOGGER.info(f'{file_name} was deleted')

        FTP_LOGGER.info(f'Uploaded files: {files_cnt}\n')
    except:
        FTP_LOGGER.error(get_raised_error(True))
    finally:
        if ftp_connected:
            ftp.quit()


if __name__ == '__main__':
    if sys.version_info < (3, 8):
        panic('We need minimum Python version 3.8 to run. Current version: %s.%s.%s' % sys.version_info[:3])

    args = create_argparse()

    if (not args.get_sales) and (not args.upload_to_ftp):
        panic('Specify -g or/and -u option. See --help for details')

    DEFAULT_LOGGER.info(f'{SOFTWARE_VERSION} started')
    DEFAULT_LOGGER.info(f'Config loaded from {CFG_FILE}\n')

    if args.get_sales:
        if (not args.beg_date) or (not args.end_date):
            panic('Specify -b and -e options. See --help for details')

        beg = datetime.strptime(args.beg_date, DATE_FORMAT_FULL)
        end = datetime.strptime(args.end_date, DATE_FORMAT_FULL)
        download_sales(beg, end)

    if args.upload_to_ftp:
        upload_files(args.delete_uploaded_files)

    DEFAULT_LOGGER.info(f'{APP_NAME} stopped\n')
