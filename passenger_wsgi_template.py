import sys, os

VENV=None

if VENV is not None:
    INTERP = os.path.join(VENV, 'bin', 'python')
    if sys.executable != INTERP:
        os.execl(INTERP, INTERP, *sys.argv)

from {{ appname }} import app as application
