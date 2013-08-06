'''Pipeline

(yield) -> receiver
.send -> producer

Provide initial state to producer, avoiding globals.
Stop iteration after a bit.
Wrap in nice class.
Simple crawler to check if "python" was mentioned on HN.
Some improvements after: http://www.dabeaz.com/Fcoroutines/Coroutines.pdf
    - coroutine decorator
    - catch GeneratorExit
'''
# TODO: add cycle pipe


from decorators import consumer, stage, Producer, broadcast
from utils import validate


class Pipeline(object):

    def __init__(self, producer_func, stages, consumer_func, validator=validate):
        '''constructs the pipeline'''
        self._validator = validator
        self._pipeline = consumer(consumer_func)

        while stages:
            self._pipeline = stage(stages.pop(), self._pipeline, self._validator)

        self._pipeline = Producer(producer_func, self._pipeline, self._validator)

    def follow(self, initial_state):
        try:
            self._pipeline.send(initial_state)
        except StopIteration:
            self._pipeline.close()


class BranchedPipeline(Pipeline):

    def __init__(self, producer_func, stages, branches, validator=validate):
        '''constructs the pipeline'''
        self._validator = validator
        self._pipeline = broadcast(branches)

        while stages:
            self._pipeline = stage(stages.pop(), self._pipeline, self._validator)

        self._pipeline = Producer(producer_func, self._pipeline, self._validator)


class TailPipeline(Pipeline):

    def __init__(self, stages, consumer_func, validator=validate):
        '''constructs the pipeline'''
        self._validator = validator
        self._pipeline = consumer(consumer_func)

        while stages:
            self._pipeline = stage(stages.pop(), self._pipeline, self._validator)


class ExtentionPipeline(Pipeline):

    def __init__(self, stages, validator=validate):
        '''constructs the pipeline'''
        self._validator = validator
        self._pipeline = consumer(lambda x: x)
        while stages:
            self._pipeline = stage(stages.pop(), self._pipeline, self._validator)
