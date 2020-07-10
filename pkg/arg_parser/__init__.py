import argparse
from pkg.constants.version import SOFTWARE_VERSION


def create_argparse():
    parser = argparse.ArgumentParser(description=SOFTWARE_VERSION)
    parser.add_argument(
        '-b',
        '--beg-date',
        help=f'Beginning of period, mandatory if -g specified (dd.mm.yyyy hh24:mi:ss)'
    )
    parser.add_argument(
        '-e',
        '--end-date',
        help='End of period, mandatory if -g specified (dd.mm.yyyy hh24:mi:ss)'
    )
    parser.add_argument(
        '-y',
        '--yesterday',
        action='store_true',
        help='Set period as yesterday'
    )
    parser.add_argument(
        '-g',
        '--get-sales',
        action='store_true',
        help='Get sales from UMAG'
    )
    parser.add_argument(
        '-u',
        '--upload-to-ftp',
        action='store_true',
        help='Upload XML files to FTP-server'
    )
    parser.add_argument(
        '-d',
        '--delete-uploaded-files',
        action='store_true',
        help='Delete XML files which was successfully uploaded to FTP-server'
    )
    parser.add_argument(
        '-c',
        '--config-file',
        help='Full path to YAML config file'
    )
    return parser.parse_args()
