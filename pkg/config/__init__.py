import os
import yaml
from pkg.utils.console import panic
from pkg.utils.files import read_file

try:
    CFG_FILE = os.environ.get('SHYM_PLAZA_CONFIG', None) or 'config.yml'
    CONFIG = yaml.load(read_file(CFG_FILE), Loader=yaml.BaseLoader)
except FileNotFoundError:
    panic()
