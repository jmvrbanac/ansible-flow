import sys
import subprocess

from ansibleflow.config import config
from ansibleflow.venv import env_path


def run(name, arguments):
    pass


def argument_handler(value, all_args):
    if value == True:
        print('Please specify a environment to run...')
        sys.exit(1)

    run(value[0], all_args)
