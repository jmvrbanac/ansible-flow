import argparse

from ansibleflow import venv, run, rekey


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

    rekey_parser = subparsers.add_parser('rekey')
    rekey_parser.add_argument(
        '--orig-key',
        type=str,
        required=True,
        metavar='path',
        help='Filename for the original vault key'
    )
    rekey_parser.add_argument(
        '--new-key',
        type=str,
        required=True,
        metavar='path',
        help='Filename for the new vault key'
    )
    rekey_parser.add_argument('filename', type=str, metavar='file_path')
    rekey_parser.add_argument(
        'rekey_action',
        nargs='*',
        default=True,
        help=argparse.SUPPRESS
    )

    run_parser = subparsers.add_parser('run')
    run_parser.add_argument('--env', type=str, default='default')
    run_parser.add_argument(
        'run_action',
        nargs='*',
        default=True,
        help=argparse.SUPPRESS
    )

    return parser


def main(args=None, venv_handler=None, run_handler=None, rekey_handler=None):
    parser = setup_argument_parser()

    mapping = {
        'venv_action': venv_handler or venv.argument_handler,
        'run_action': run_handler or run.argument_handler,
        'rekey_action': rekey_handler or rekey.argument_handler,
    }

    mapper = ArgumentMapper(mapping, parser, args)
    mapper.execute()


if __name__ == "__main__":
    main()
