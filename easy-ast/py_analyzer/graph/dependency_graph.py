import networkx as nx
from pydantic import BaseModel, Field

from py_analyzer.code2.code_base import CodeBase
from py_analyzer.constants import STD_LIB


class DependencyConfig(BaseModel):
    keep_unknown: bool = False
    keep_functions: bool = False
    keep_constants: bool = False
    keep_classes: bool = False
    ignore: set[str] = Field(default_factory=set)


class DependencyGraph:
    def __init__(self, name: str, config: DependencyConfig = None):
        self.graph = nx.DiGraph()
        self.config = config or DependencyConfig(ignore={
            *STD_LIB
        })

    def load(self, code: CodeBase):

        def category(path: str):
            try:
                return path.split('.')[0]
            except:
                return path

        for name, module in code.modules.items():
            for i in module.parsing.imports:
                for ignored in self.config.ignore:
                    if i.startswith(ignored):
                        continue
                if not self.config.keep_unknown and not code.hierarchy.is_present(i):
                    print(f'ignoring: {i}')
                    continue
                if not self.config.keep_functions and i in code.stats.functions:
                    continue
                if not self.config.keep_constants and i in code.stats.constants:
                    continue

                if not self.config.keep_classes and i in code.stats.classes:
                    continue
                self.graph.add_node(name, category=category(name))
                self.graph.add_node(i, category=category(i))
                self.graph.add_edge(name, i)

        return self

    def draw(self):
        import holoviews as hv

        hv.extension('bokeh')
        graph = hv.Graph.from_networkx(
            self.graph,
            nx.nx_pydot.graphviz_layout,
            prog='neato'
        ).opts(
            tools=['hover'],
            directed=True,
            node_size=25,
            arrowhead_length=0.002,
            responsive=True,
            node_color='category',
            cmap='Set1',
            edge_line_width=1,
        )

        # from holoviews.operation.datashader import bundle_graph
        # graph = bundle_graph(graph)

        labels = hv.Labels(
            graph.nodes,
            ['x', 'y'],
            'index',
        ).opts(
            text_font_size='8pt',
            text_color='white',
            bgcolor='gray'
        )
        graph_labels = (graph * labels)

        hv.save(graph_labels, 'app.html')
