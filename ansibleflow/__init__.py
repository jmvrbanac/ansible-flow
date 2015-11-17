import sys

SUPPRESS_OUTPUT = False


def log(output, newline=True):
    if not SUPPRESS_OUTPUT:
        full_output = output.encode('utf-8')
        if newline:
            full_output += '\n'
        sys.stdout.write(full_output)
