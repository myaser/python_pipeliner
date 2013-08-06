import unittest
from __init__ import Pipeline, BranchedPipeline, ExtentionPipeline, TailPipeline
from utils import StopPipeline


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
        p.follow(0)
        desired_trace = [
        ("provider", 0), ("stage1", 0), ("stage2", 0), ("consumer", 0),
        ("provider", 1), ("stage1", 1), ("stage2", 1), ("consumer", 1),
        ("provider", 2), ("stage1", 2), ("stage2", 2), ("consumer", 2),
        ("provider", 3), ("stage1", 3), ("stage2", 3), ("consumer", 3),
        ("provider", 4), ("stage1", 4), ("stage2", 4), ("consumer", 4),
                         ]
        self.assertEqual(self.trace, desired_trace)


class TestBranchedPipeline(TestPipeline):

    def test_pipeline(self):
        p1 = TailPipeline([self.stage1, self.stage2], self.consumer, self.validate)
        p2 = TailPipeline([self.stage1, self.stage2], self.consumer, self.validate)
        p = BranchedPipeline(self.provider, [self.stage1, self.stage2], [p1, p2], self.validate)

        p.follow(0)
        desired_trace = [
        ('provider', 0), ('stage1', 0), ('stage2', 0),
            ('stage1', 0), ('stage2', 0), ('consumer', 0),
            ('stage1', 0), ('stage2', 0), ('consumer', 0),
        ('provider', 1), ('stage1', 1), ('stage2', 1),
            ('stage1', 1), ('stage2', 1), ('consumer', 1),
            ('stage1', 1), ('stage2', 1), ('consumer', 1),
        ('provider', 2), ('stage1', 2), ('stage2', 2),
            ('stage1', 2), ('stage2', 2), ('consumer', 2),
            ('stage1', 2), ('stage2', 2), ('consumer', 2),
        ('provider', 3), ('stage1', 3), ('stage2', 3),
            ('stage1', 3), ('stage2', 3), ('consumer', 3),
            ('stage1', 3), ('stage2', 3), ('consumer', 3),
        ('provider', 4), ('stage1', 4), ('stage2', 4),
            ('stage1', 4), ('stage2', 4), ('consumer', 4),
            ('stage1', 4), ('stage2', 4), ('consumer', 4)
        ]
        self.assertEqual(self.trace, desired_trace)


class TestExtentionPipeline(TestPipeline):

    def test_pipeline(self):
        p1 = ExtentionPipeline([self.stage1, self.stage2], self.validate)
        p2 = TailPipeline([], self.consumer, self.validate)
        p = BranchedPipeline(self.provider, [], [p1, p2], self.validate)

        p.follow(0)
        desired_trace = [
        ("provider", 0), ("stage1", 0), ("stage2", 0), ("consumer", 0),
        ("provider", 1), ("stage1", 1), ("stage2", 1), ("consumer", 1),
        ("provider", 2), ("stage1", 2), ("stage2", 2), ("consumer", 2),
        ("provider", 3), ("stage1", 3), ("stage2", 3), ("consumer", 3),
        ("provider", 4), ("stage1", 4), ("stage2", 4), ("consumer", 4),
                         ]
        self.assertEqual(self.trace, desired_trace)


if __name__ == '__main__':
    unittest.main()
