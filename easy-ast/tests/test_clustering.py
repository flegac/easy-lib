from unittest import TestCase

from py_analyzer.code2.hierarchy.hierarchic_clustering import HierarchicClustering
from py_analyzer.code2.hierarchy.hierarchy import Hierarchy


class TestClustering(TestCase):

    def test_cluster(self):
        x = Hierarchy().load_all({
            'a.b.c',
            'a.b.d',
            'b.c.d',
            'b.d.e'
        })
        clustering = HierarchicClustering(depth=2)
        for _ in x.iter():
            print(f'{clustering.cluster(_)}: {_}')
