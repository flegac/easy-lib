from unittest import TestCase

from py_analyzer.code2.hierarchy.hierarchy import Hierarchy


class TestHierarchy(TestCase):

    def test_is_present(self):
        x = Hierarchy()

        expected = {
            'a.b.c',
            'a.b.d',
            'b.c.d',
            'b.d.e'
        }

        for _ in expected:
            x.register(_)

        actual = {_ for _ in expected if x.is_present(_)}

        self.assertSetEqual(expected, actual)
