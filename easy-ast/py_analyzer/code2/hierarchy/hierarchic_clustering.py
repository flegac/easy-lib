from py_analyzer.graph.clustering import Clustering


class HierarchicClustering(Clustering):
    def __init__(self, depth: int):
        self.depth = depth

    def cluster(self, node: str) -> str:
        parts = node.split('.', maxsplit=self.depth + 1)
        return '.'.join(parts[:self.depth])
