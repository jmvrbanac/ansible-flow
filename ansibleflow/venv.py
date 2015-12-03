import os
import shutil
import subprocess
import virtualenv as venv

from ansibleflow import log
from ansibleflow.config import get_config
from capturer import CaptureOutput

DEFAULT_VENV_DIR = '.venv'
ENV_PATH = os.path.abspath('./{0}'.format(DEFAULT_VENV_DIR))


def env_exists():
    return os.path.exists(ENV_PATH)


def execute_under_env(command, os_env=None):
    """Completely ghetto way of executing commands under a virtualenv."""
    activate_cmd = 'source {0}/bin/activate\n'.format(ENV_PATH)
    long_cmd = '{0}; exit\n'.format(command)

    env_vars = {}
    env_vars.update(os.environ)

    if os_env:
        env_vars.update(os_env)

    with CaptureOutput():
        proc = subprocess.Popen(
            ['/bin/bash'],
            stdin=subprocess.PIPE,
            env=env_vars
        )

        proc.stdin.write(activate_cmd.encode('utf-8'))
        proc.stdin.flush()
        proc.stdin.write(long_cmd.encode('utf-8'))
        proc.stdin.flush()

        proc.wait()


def create_env():
    if env_exists():
        raise Exception('Virtual environment already exists.')

    log('Creating virtual environment...')

    home_dir, lib_dir, inc_dir, bin_dir = venv.path_locations(ENV_PATH)
    python_loc = venv.install_python(
        home_dir,
        lib_dir,
        inc_dir,
        bin_dir,
        site_packages=False,
        clear=False,
        symlink=True
    )

    python_abs_loc = os.path.abspath(python_loc)

    venv.install_activate(home_dir, bin_dir)
    venv.install_wheel(['setuptools', 'pip'], python_abs_loc, None)
    venv.install_distutils(home_dir)

    log('Installing requirements...')
    req_cmd = '{0}/bin/pip install {1}'.format(
        ENV_PATH,
        get_config().requirements
    )
    execute_under_env(req_cmd)

    log('Virtual environment created!')


def delete_env():
    shutil.rmtree(ENV_PATH)
    log('Virtual environment deleted!')


def recreate_env():
    if env_exists():
        delete_env()

    create_env()


def argument_handler(value, all_args):
    if value == 'create':
        create_env()
    elif value == 'delete':
        delete_env()
    elif value == 'recreate':
        recreate_env()
