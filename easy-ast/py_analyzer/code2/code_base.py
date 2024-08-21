from pathlib import Path

from pydantic import BaseModel, Field

from py_analyzer.code2.code_filter import CodeFilter
from py_analyzer.code2.hierarchy.hierarchy import Hierarchy
from py_analyzer.code2.module import Module
from py_analyzer.code2.parser.code_stats import CodeStats


class CodeBase(BaseModel):
    modules: dict[str, Module] = Field(default_factory=dict)
    stats: CodeStats | None = None
    hierarchy: Hierarchy = Field(default_factory=Hierarchy)

    def explore(self, root: Path, current: Path = None):
        if current is None:
            current = root
        for path in current.iterdir():
            if path.suffix == '.py':
                module = Module(root=root, path=path)
                self.modules[module.name] = module
            if path.is_dir():
                self.explore(root, path)

    def update(self):
        self._update_parsing()
        self._update_hierarchy()

    def _update_parsing(self):
        self.stats = CodeStats()
        for _, module in self.modules.items():
            module.update()
            self.stats.load(module.parsing)
        return self

    def _update_hierarchy(self):
        self.hierarchy.clear()
        for name, module in self.modules.items():
            for item in module.parsing.iter_all():
                self.hierarchy.register(item)

        return self

    def extract(self, selector: CodeFilter):
        hierarchy = Hierarchy()

    def keep_only(self, *prefixes: str):
        return CodeBase(modules={
            k: v
            for k, v in self.modules.items()
            if any([k.startswith(prefix) for prefix in prefixes])
        })

    def remove_all(self, *prefixes: str):
        return CodeBase(modules={
            k: v
            for k, v in self.modules.items()
            if not any([k.startswith(prefix) for prefix in prefixes])
        })

    def __repr__(self):
        return f'modules:{len(self.modules)}'

    def __str__(self):
        return repr(self)
