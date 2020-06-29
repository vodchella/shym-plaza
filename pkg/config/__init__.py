import os
import yaml
from pkg.arg_parser import create_argparse
from pkg.utils import get_project_root
from pkg.utils.console import panic
from pkg.utils.files import read_file

os.chdir(get_project_root())
args = create_argparse()
try:
    if args.config_file:
        CFG_FILE = args.config_file
    else:
        CFG_FILE = os.environ.get('SHYM_PLAZA_CONFIG', None) or 'config.yml'
    CONFIG = yaml.load(read_file(CFG_FILE), Loader=yaml.BaseLoader)
except FileNotFoundError:
    panic()
