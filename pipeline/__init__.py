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


from .decorators import consumer, stage, Producer
from .utils import validate


class Pipeline(object):

    def __init__(self, producer_func, stages, consumer_func, validator=validate):
        '''constructs the pipeline'''
        self._validator = validator
        self._pipeline = consumer(consumer_func)

        while stages:
            self._pipeline = stage(stages.pop(), self._pipeline, self._validator)

        self._pipeline = Producer(producer_func, self._pipeline, self._validator)

    def follow(self, initial_state):
        res = []
        try:
            while True:
                res.append(self._pipeline.send(initial_state))
        except StopIteration:
            self._pipeline.close()
            return res
