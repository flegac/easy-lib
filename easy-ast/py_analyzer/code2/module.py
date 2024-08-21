import ast
from pathlib import Path

from pydantic import BaseModel

from py_analyzer.code2.parser.code_stats import CodeStats
from py_analyzer.code2.parser.stat_parser import StatParser


class Module(BaseModel):
    root: Path
    path: Path
    parsing: CodeStats | None = None

    @property
    def name(self):
        rel_path = self.path.relative_to(self.root)
        return str(rel_path.parent / rel_path.stem).replace('\\', '.').replace('/', '.')

    def to_path(self, name: str):
        rel_path = name.replace('.', '/')
        return self.root / f'{rel_path}.py'

    def update(self):
        node = self._ast_node()
        parser = StatParser()
        parser.visit(node)
        parser.stats.modules.add(self.name)
        self.parsing = parser.stats

    def _ast_node(self):
        try:
            with self.path.open() as _:
                code = _.read()
                return ast.parse(code, str(self.path))
        except Exception as e:
            print(f'ERROR:{self.path}: {e}')
            raise e

    def __repr__(self):
        return f'{self.parsing} [{self.name:45}]'

    def __str__(self):
        return repr(self)
