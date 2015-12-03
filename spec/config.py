from ansibleflow import config
from specter import Spec, expect


def build_target_obj(overrides=None):
    target_dict = {
        'playbooks': ['play.yml'],
        'inventory': 'inventory.ini',
        'tags': 'nope',
        'ansible-options': '-vvvv',
    }
    if overrides:
        target_dict.update(overrides)

    return config.Target.from_dict('bam', target_dict)


def build_env_obj(overrides=None):
    env_dict = {
        'vault-key': './vault-key',
        'custom-var-files': ['thing.yml'],
        'directory': 'random_dir',
        'ansible-config': 'ansible.cfg',
        'shell-variables': {'trace': 'boom'},
    }
    if overrides:
        env_dict.update(overrides)

    return config.Environment.from_dict('bam', env_dict)


class ConfigModuleTests(Spec):

    def can_build_a_target_from_a_dictionary(self):
        obj = build_target_obj()

        expect(obj.name).to.equal('bam')
        expect('play.yml').to.be_in(obj.playbooks)
        expect(obj.inventory).to.equal('inventory.ini')
        expect(obj.tags).to.equal('nope')
        expect(obj.options).to.equal('-vvvv')

    def can_build_a_environment_from_a_dictionary(self):
        obj = build_env_obj()

        expect(obj.name).to.equal('bam')
        expect(obj.vault_key).to.equal('./vault-key')
        expect('thing.yml').to.be_in(obj.custom_var_files)
        expect(obj.directory).to.equal('random_dir')
        expect(obj.ansible_config).to.equal('ansible.cfg')
        expect(obj.shell_vars).to.equal({'trace': 'boom'})

    def can_load_a_config_from_file(self):
        cfg = config.get_config('./data/test_project.yml')
        config._config = None
        expect(cfg).not_to.be_none()

    def non_existant_config_should_system_exit(self):
        try:
            config.config_exists('/trace/blarg')
        except SystemExit:
            expect(True).to.be_true()

    class UsingTheConfigObject(Spec):
        def before_each(self):
            self.cfg = config.get_config('./data/test_project.yml')
            config._config = None

        def can_access_the_enviroments_property(self):
            envs = self.cfg.environments
            expect('dev').to.be_in(envs)
            expect('default').to.be_in(envs)

        def can_access_the_targets_property(self):
            envs = self.cfg.targets
            expect('create').to.be_in(envs)

        def can_access_the_requirements_property(self):
            expect(self.cfg.requirements).to.equal('ansible==1.9.4')
