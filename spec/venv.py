import os
import shutil
import tempfile

import ansibleflow
from ansibleflow import venv
from spec import BaseSpec
from specter import Spec, expect


class VirtualEnvTests(BaseSpec):
    def can_get_env_path(self):
        path = venv.ENV_PATH
        expect('/.venv').to.be_in(path)

    def invalid_argument_does_nothing(self):
        venv.argument_handler('boom', None)

    class VirtualEnvHandling(Spec):
        def before_each(self):
            ansibleflow.SUPPRESS_OUTPUT = True
            self._old_env_path = venv.ENV_PATH

            # Create a place for our test virtualenv
            self._temp_path = tempfile.mkdtemp()
            venv.ENV_PATH = os.path.join(self._temp_path, '.venv')

        def after_each(self):
            venv.ENV_PATH = self._old_env_path
            shutil.rmtree(self._temp_path)
            ansibleflow.SUPPRESS_OUTPUT = False

        def can_create_and_delete(self):
            venv.argument_handler('create', None)
            expect(os.path.exists(venv.ENV_PATH)).to.be_true()

            venv.argument_handler('delete', None)
            expect(os.path.exists(venv.ENV_PATH)).to.be_false()

        def can_recreate(self):
            # Calling without an environment existing
            venv.argument_handler('recreate', None)
            expect(os.path.exists(venv.ENV_PATH)).to.be_true()

            # Calling again now that the environment exists
            venv.argument_handler('recreate', None)
            expect(os.path.exists(venv.ENV_PATH)).to.be_true()

        def cannot_create_when_an_env_already_exists(self):
            venv.create_env()
            expect(venv.create_env).to.raise_a(Exception)
