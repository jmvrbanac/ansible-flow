import os
import sys

import yaml

_config = None


class Target(object):
    def __init__(self, name, playbooks, inventory=None, tags=None,
                 options=None):
        self.name = name
        self.playbooks = playbooks
        self.inventory = inventory
        self.tags = tags
        self.options = options

    @classmethod
    def from_dict(cls, name, input_dict):
        return Target(
            name,
            input_dict.get('playbooks', None),
            input_dict.get('inventory', None),
            input_dict.get('tags', None),
            input_dict.get('ansible-options', None)
        )


class Environment(object):
    def __init__(self, name, vault_key=None, custom_vars=None, directory=None,
                 ansible_config=None, shell_vars=None):
        self.name = name
        self.vault_key = vault_key
        self.custom_var_files = custom_vars
        self.directory = directory
        self.ansible_config = ansible_config
        self.shell_vars = shell_vars

    @classmethod
    def from_dict(cls, name, input_dict):
        return Environment(
            name,
            input_dict.get('vault-key', None),
            input_dict.get('custom-var-files', None),
            input_dict.get('directory', None),
            input_dict.get('ansible-config', None),
            input_dict.get('shell-variables', None)
        )


class Config(object):

    def __init__(self, yml_cfg):
        self._config = yml_cfg

    @property
    def environments(self):
        converted = {}
        environments_dict = self._config.get('environments', {})
        default_env_dict = environments_dict.get('default')

        for name, env_dict in environments_dict.items():
            # Environment settings on a default environment
            working_dict = {}
            working_dict.update(default_env_dict)
            working_dict.update(env_dict)

            environment = Environment.from_dict(name, working_dict)
            converted[name] = environment
        return converted

    @property
    def targets(self):
        converted = {}
        for name, target_dict in self._config.get('targets', {}).items():
            target = Target.from_dict(name, target_dict)
            converted[name] = target
        return converted

    @property
    def requirements(self):
        raw_req = self._config.get('requirements', [])
        req_str = ' '.join(raw_req)

        return req_str


def config_exists(filename):
    if not os.path.exists(filename):
        print('Error: Could not file project configuration!')
        sys.exit(1)


def load_config(filename):
    document = None

    config_exists(filename)

    with open(filename, 'r') as data_file:
        document = yaml.load(data_file.read())

    return Config(document)


def get_config(filename='./project.yml'):
    global _config  # Ugly, but it works for now

    if not _config:
        _config = load_config(os.path.abspath(filename))
    return _config
