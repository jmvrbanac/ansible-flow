from ansibleflow import app, config
from specter import expect
from spec import BaseSpec


class Application(BaseSpec):
    def can_create_argparse_parser(self):
        parser = app.setup_argument_parser()
        expect(parser).not_to.be_none()

    def can_execute_main(self):
        try:
            app.main([])
        except SystemExit:
            expect('too few arguments').to.be_in(self.stderr.getvalue())

    def run_requires_a_target(self):
        try:
            app.main(['run'])
        except SystemExit:
            err_msg = 'Please specify a target to run...'
            expect(err_msg).to.be_in(self.stdout.getvalue())

    def run_requires_a_project_cfg(self):
        config._config = None

        try:
            app.main(['run', 'bam'])
        except SystemExit:
            err_msg = 'Error: Could not file project configuration!'
            expect(err_msg).to.be_in(self.stdout.getvalue())

    def run_requires_a_venv(self):
        config.get_config('./data/test_project.yml')

        try:
            app.main(['run', 'bam'])
        except SystemExit:
            err_msg = ('Virtual environment does not exist.. '
                       'Please run: ansible-flow venv create')
            expect(err_msg).to.be_in(self.stdout.getvalue())
