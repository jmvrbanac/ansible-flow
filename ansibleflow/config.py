import os
import sys

import yaml


class Config(object):

    def __init__(self, yml_cfg):
        self._config = yml_cfg

    @property
    def environments(self):
        return self._config.get('environments', [])

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
