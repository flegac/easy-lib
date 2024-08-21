from pathlib import Path

from py_analyzer.code2.code_base import CodeBase
from py_analyzer.constants import KEEP_ONLY, STD_LIB
from py_analyzer.graph.dependency_graph import DependencyGraph

ROOT = Path.cwd().parent.parent

if __name__ == '__main__':
    code = CodeBase()
    code.explore(root=ROOT / 'easy-lib')
    # code.explore(root=ROOT / 'sandbox-3d')
    # code.explore(root=ROOT / 'python-ecs')

    selection = code.keep_only(*KEEP_ONLY).remove_all(*STD_LIB).remove_all('tests', 'setup')
    selection.update()

    selection.stats.print_debug()

    dependencies = DependencyGraph('graph').load(selection)

    dependencies.draw()

    # HierarchicClustering(depth=1).draw(dependencies.graph)
