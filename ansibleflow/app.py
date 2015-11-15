import argparse

from ansibleflow import config, venv, run


class ArgumentMapper(object):
    def __init__(self, mapping, parser, args=None):
        self._mapping = mapping
        self._parser = parser
        self._args = self._parser.parse_args(args)

    def execute(self):
        for arg_name, func in self._mapping.items():
            arg = getattr(self._args, arg_name, None)
            if arg:
                func(arg, self._args)


def setup_argument_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    env_parser = subparsers.add_parser('venv')
    env_parser.add_argument(
        'venv_action',
        choices=['create', 'delete', 'recreate'],
    )

    run_parser = subparsers.add_parser('run')
    run_parser.add_argument(
        'run_action',
        nargs='*',
        default=True,
        help=argparse.SUPPRESS
    )

    return parser


def main():
    parser = setup_argument_parser()

    mapping = {
        'venv_action': venv.argument_handler,
        'run_action': run.argument_handler,
    }

    mapper = ArgumentMapper(mapping, parser)
    mapper.execute()


if __name__ == "__main__":
    main()
