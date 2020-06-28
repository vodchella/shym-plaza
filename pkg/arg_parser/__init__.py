import argparse
from pkg.constants.version import SOFTWARE_VERSION


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
        help='Upload xml files to ftp-server'
    )
    return parser.parse_args()
