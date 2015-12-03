import sys

from ansibleflow import config
from specter import Spec, fixture
from six import StringIO


real_stdout = sys.stdout
real_stderr = sys.stderr


@fixture
class BaseSpec(Spec):

    def before_all(self):
        config.get_config('./data/test_project.yml')

    def after_all(self):
        config._config = None

    def before_each(self):
        sys.stdout = self.stdout = StringIO()
        sys.stderr = self.stderr = StringIO()

    def after_each(self):
        sys.stdout = real_stdout
        sys.stderr = real_stderr
