import sys
import subprocess

from ansibleflow.config import config
from ansibleflow.venv import execute_under_env


def build_ansible_command(target, environment):
    command = 'ansible-playbook'

    if environment.custom_var_files:
        for filename in environment.custom_var_files:
            command += ' -e @./{0}'.format(filename)
    if environment.vault_key:
        command += ' --vault-password-file {0}'.format(environment.vault_key)

    command += ' {0}'.format(target.playbook)

    if target.tags:
        command += ' --tags "{0}"'.format(target.tags)

    return command


def run(target_name, env_name, arguments):
    target = config.targets.get(target_name, None)
    environment = config.environments.get(env_name, None)

    if not target:
        print('Could not find target: {0}'.format(target_name))
        sys.exit(1)

    if not environment:
        print('Could not find environment: {0}'.format(env_name))
        sys.exit(1)

    print(build_ansible_command(target, environment))



def argument_handler(value, all_args):
    if value == True:
        print('Please specify a target to run...')
        sys.exit(1)

    run(value[0], all_args.env, all_args)
