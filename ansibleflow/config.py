import os
import sys

import yaml


class Target(object):
    def __init__(self, name, playbook, tags=None):
        self.name = name
        self.playbook = playbook
        self.tags = tags

    @classmethod
    def from_dict(cls, name, input_dict):
        return Target(
            name,
            input_dict.get('playbook', None),
            input_dict.get('tags', None)
        )


class Environment(object):
    def __init__(self, name, vault_key=None, custom_vars=None):
        self.name = name
        self.vault_key = vault_key
        self.custom_var_files = custom_vars

    @classmethod
    def from_dict(cls, name, input_dict):
        return Environment(
            name,
            input_dict.get('vault-key', None),
            input_dict.get('custom-var-files', None)
        )


class Config(object):

    def __init__(self, yml_cfg):
        self._config = yml_cfg

    @property
    def environments(self):
        converted = {}
        for name, env_dict in self._config.get('environments', {}).items():
            environment = Environment.from_dict(name, env_dict)
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


config = load_config(os.path.abspath('./project.yml'))
