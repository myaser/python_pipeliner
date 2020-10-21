from .utils import close_on_exit, StopPipeline


def coroutine(func):
    def start(*args, **kwargs):
        coroutine = func(*args, **kwargs)
        next(coroutine)
        return coroutine
    return start


@coroutine
def Producer(func, next_stage, validate):
    '''Producer: only .send (and yield as entry point).'''

    state = (yield)  # get initial state
    with close_on_exit(next_stage):
        while True:
            try:
                res, state = func(state)
            except StopPipeline:
                return
            if validate(res):
                yield next_stage.send(res)


@coroutine
def stage(func, next_stage, validate):
    '''Stage: both (yield) and .send.'''

    data = None
    with close_on_exit(next_stage):
        while True:
            data = (yield data)
            data = func(data)
            if validate(data):
                data = next_stage.send(data)


@coroutine
def broadcast(pipelines):
    '''Stage: both (yield) and .send.'''

    while True:
        data = (yield)
        for pipeline in pipelines:
            pipeline.follow(data)


@coroutine
def consumer(func):
    '''Consumer: only (yield).'''

    data = None

    # nothing to "close" here
    while True:
        data = (yield data)
        data = func(data)
