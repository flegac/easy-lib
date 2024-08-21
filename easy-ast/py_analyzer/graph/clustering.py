from abc import ABC, abstractmethod
from collections import defaultdict

from py_analyzer.graph.graph import Graph


class Clustering(ABC):
    @abstractmethod
    def cluster(self, node: str) -> str:
        ...

    def draw(self, graph: Graph):
        clusters = defaultdict(set)

        for source in graph.nodes:
            clusters[self.cluster(source)].add(source)
        clusters = dict(clusters)

        cluster_graph = Graph(name='clusters')
        for source in graph.nodes:
            for target in graph.links(source):
                cluster_graph.link(self.cluster(source), self.cluster(target))

        parent = cluster_graph.graph()
        
        for name, cluster in clusters.items(): 
            g = Graph(name=name)
            for node in cluster:
                for n in graph.links(node):
                    if self.cluster(n) == name:
                        g.link(node, n)
    
            with parent.subgraph(name=f'cluster_{name}') as c:
                c.attr(label=name)
                g.graph(c)                

        cluster_graph.draw(parent)
