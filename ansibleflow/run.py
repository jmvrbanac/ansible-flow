import os
import sys

from ansibleflow import log
from ansibleflow.config import get_config
from ansibleflow.venv import execute_under_env


def convert_var_filename_to_arg(filename, environment):
    file_path = filename
    if environment.directory:
        file_path = os.path.join(environment.directory, filename)

    return ' -e @{0}'.format(os.path.abspath(file_path))


def build_ansible_command(target, environment):
    command = 'ansible-playbook'

    if target.inventory:
        command += ' -i {0}'.format(os.path.abspath(target.inventory))

    if environment.custom_var_files:
        for filename in environment.custom_var_files:
            command += convert_var_filename_to_arg(filename, environment)

    if environment.vault_key:
        command += ' --vault-password-file {0}'.format(environment.vault_key)

    command += ' {0}'.format(target.playbook)

    if target.tags:
        command += ' --tags "{0}"'.format(target.tags)

    return command


def run(target_name, env_name, arguments, dry_run=False):
    target = get_config().targets.get(target_name, None)
    environment = get_config().environments.get(env_name, None)

    if not target:
        log('Could not find target: {0}'.format(target_name))
        sys.exit(1)

    if not environment:
        log('Could not find environment: {0}'.format(env_name))
        sys.exit(1)

    command = build_ansible_command(target, environment)
    log(command)

    if not dry_run:
        os_env = None
        if environment.ansible_config:
            os_env = {'ANSIBLE_CONFIG': environment.ansible_config}

        execute_under_env(command, os_env)

def argument_handler(value, all_args):
    if value is True:
        log('Please specify a target to run...')
        sys.exit(1)

    run(value[0], all_args.env, all_args)
