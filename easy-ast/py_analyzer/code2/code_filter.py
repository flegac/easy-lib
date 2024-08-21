from py_analyzer.code2.hierarchy.hierarchy import Hierarchy


class CodeFilter:
    def __init__(self, keep_only: set[str], exclude: set[str]):
        self.keep_only = Hierarchy().load_all(keep_only)
        self.exclude = Hierarchy().load_all(exclude)

    def accept(self, name: str):
        return all([
            self.keep_only.is_present(name),
            not self.exclude.is_present(name)
        ])
