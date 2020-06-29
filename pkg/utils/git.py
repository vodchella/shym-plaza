import os
from pkg.utils import get_project_root

git = None
try:
    from sh import git
except:
    pass


def get_top_commit(short: bool = True):
    if git:
        try:
            os.chdir(get_project_root())
            commit = git('rev-parse', '--short', 'HEAD') if short else git('rev-parse', 'HEAD')
            return commit.strip('\n')
        except:
            pass
