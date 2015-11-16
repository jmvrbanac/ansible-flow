SUPPRESS_OUTPUT = False


def log(output):
    if not SUPPRESS_OUTPUT:
        print(output.encode('utf-8'))
