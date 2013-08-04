from utils import close_on_exit, StopPipeline


def coroutine(func):
    def start(*args, **kwargs):
        coroutine = func(*args, **kwargs)
        coroutine.next()
        return coroutine
    return start


@coroutine
def Producer(func, next_stage):
    '''Producer: only .send (and yield as entry point).'''

    state = (yield)  # get initial state
    with close_on_exit(next_stage):
        while True:
            try:
                res, state = func(state)
            except StopPipeline:
                return
            next_stage.send(res)


@coroutine
def stage(func, next_stage):
    '''Stage: both (yield) and .send.'''

    with close_on_exit(next_stage):
        while True:
            data = (yield)
            next_stage.send(func(data))


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

    # nothing to "close" here
    while True:
        data = (yield)
        func(data)
