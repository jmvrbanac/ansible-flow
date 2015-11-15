import os
import shutil
import subprocess
import virtualenv as venv

from ansibleflow.config import config

DEFAULT_VENV_DIR = '.venv'


def env_path():
    return os.path.abspath('./{0}'.format(DEFAULT_VENV_DIR))


def env_exists():
    return os.path.exists(env_path())


def execute_under_env(command):
    """Completely ghetto way of executing commands under a virtualenv."""
    activate_cmd = 'source {0}/bin/activate\n'.format(env_path())
    long_cmd = '{0} && echo "!!DONE!!"\n'.format(command)

    proc = subprocess.Popen(
        ['/bin/bash'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
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
            print(output.strip())


def create_env():
    if env_exists():
        print('Virtual environment already exists.')
        return
    print('Creating virtual environment...')

    home_dir, lib_dir, inc_dir, bin_dir = venv.path_locations(env_path())
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

    print('Installing requirements...')
    req_cmd = '{0}/bin/pip install {1}'.format(env_path(), config.requirements)
    execute_under_env(req_cmd)

    print('Virtual environment created!')


def delete_env():
    shutil.rmtree(env_path())
    print('Virtual environment deleted!')


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
