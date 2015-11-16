import os
import shutil
import subprocess
import virtualenv as venv

from ansibleflow import log
from ansibleflow.config import get_config

DEFAULT_VENV_DIR = '.venv'
ENV_PATH = os.path.abspath('./{0}'.format(DEFAULT_VENV_DIR))


def env_exists():
    return os.path.exists(ENV_PATH)


def execute_under_env(command):
    """Completely ghetto way of executing commands under a virtualenv."""
    activate_cmd = 'source {0}/bin/activate\n'.format(ENV_PATH)
    long_cmd = '{0}; echo "!!DONE!!"\n'.format(command)

    proc = subprocess.Popen(
        ['/bin/bash'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    proc.stdin.write(activate_cmd)
    proc.stdin.flush()
    proc.stdin.write(long_cmd)
    proc.stdin.flush()

    while proc.poll() is None:
        output = proc.stdout.readline()

        if '!!DONE!!' in output:
            proc.stdin.write('exit\n')
        else:
            log(output.strip())


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
