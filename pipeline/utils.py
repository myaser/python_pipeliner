from contextlib import contextmanager

@contextmanager
def close_on_exit(generator):
    try:
        yield
    except GeneratorExit:
        generator.close()


class StopPipeline(Exception):
    pass