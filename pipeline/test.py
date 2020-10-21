import unittest
from . import Pipeline
from .utils import StopPipeline


class TestPipeline(unittest.TestCase):

    def setUp(self):
        def provider(num):
            if num < 5:
                self.trace.append(("provider", num))
                return num, num + 1
            else:
                raise StopPipeline("limit reached")

        def stage1(num):
            self.trace.append(("stage1", num))
            return num

        def stage2(num):
            self.trace.append(("stage2", num))
            return num

        def consumer(num):
            self.trace.append(("consumer", num))
            return num

        def validate(num):
            if num >= 0:
                return True
            return False

        self.validate = validate
        self.provider = provider
        self.stage1 = stage1
        self.stage2 = stage2
        self.consumer = consumer
        self.trace = []

    def test_pipeline(self):
        p = Pipeline(self.provider, [self.stage1, self.stage2], self.consumer, self.validate)
        self.result = p.follow(0)

        desired_result = [0, 1, 2, 3, 4]
        desired_trace = [
            ("provider", 0), ("stage1", 0), ("stage2", 0), ("consumer", 0),
            ("provider", 1), ("stage1", 1), ("stage2", 1), ("consumer", 1),
            ("provider", 2), ("stage1", 2), ("stage2", 2), ("consumer", 2),
            ("provider", 3), ("stage1", 3), ("stage2", 3), ("consumer", 3),
            ("provider", 4), ("stage1", 4), ("stage2", 4), ("consumer", 4),
        ]
        self.assertEqual(self.trace, desired_trace)
        self.assertEqual(self.result, desired_result)
