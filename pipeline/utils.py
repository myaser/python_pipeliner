from contextlib import contextmanager


@contextmanager
def close_on_exit(generator):
    try:
        yield
    except GeneratorExit:
        generator.close()


def validate(data):
    if bool(data):
        return True
    return False


class StopPipeline(Exception):
    pass
