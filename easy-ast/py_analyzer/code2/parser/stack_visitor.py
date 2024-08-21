import ast


class StackVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.max_depth = 0
    # 
    # def visit(self, node):
    #     self.stack.append(node)
    #     # self.max_depth = max(self.max_depth, len(self.stack))
    #     try:
    #         return super().visit(node)
    #     finally:
    #         self.stack.pop(-1)
