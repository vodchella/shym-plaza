from pkg.utils.git import get_top_commit


APP_NAME = 'ShymPlaza Bridge'
APP_VERSION = '0.01'


def get_app_version_full():
    commit = get_top_commit()
    commit_str = f'.{commit}' if commit else ''
    return f'{APP_VERSION}{commit_str}'


APP_VERSION_FULL = get_app_version_full()
SOFTWARE_VERSION = f'{APP_NAME} v{APP_VERSION_FULL}'
