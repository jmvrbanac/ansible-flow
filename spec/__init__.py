from specter import Spec, fixture
from ansibleflow import config


@fixture
class BaseSpec(Spec):
    def before_all(self):
        config.get_config('./data/test_project.yml')

    def after_all(self):
        config._config = None
