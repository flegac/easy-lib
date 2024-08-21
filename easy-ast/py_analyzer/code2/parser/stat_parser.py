from _ast import For, If, AST, Module, ClassDef, FunctionDef, AsyncFunctionDef, Call, Assign, Tuple, Subscript, \
    Constant, Name, Attribute, List, BinOp, UnaryOp, Lambda
from typing import Any

from loguru import logger

from py_analyzer.code2.parser.code_stats import CodeStats
from py_analyzer.code2.parser.stack_visitor import StackVisitor


class StatParser(StackVisitor):
    def __init__(self):
        super().__init__()
        self.stats = CodeStats()

    def visit_For(self, node: For) -> Any:
        self.stats.loops.add(str(node.target))
        self.generic_visit(node)

    def visit_If(self, node: If) -> Any:
        self.stats.conditions.add(str(node.test))
        self.generic_visit(node)

    def visit_Import(self, node: AST):
        for name in node.names:
            full_name = name.name
            self.stats.imports.add(full_name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: AST):
        for name in node.names:
            full_name = f'{node.module}.{name.name}'
            self.stats.imports.add(full_name)
        self.generic_visit(node)

    def visit_Module(self, node: Module) -> Any:
        self.generic_visit(node)

    def visit_ClassDef(self, node: ClassDef):
        self.stats.classes.add(node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: FunctionDef):
        self.stats.functions.add(node.name)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: AsyncFunctionDef):
        self.stats.functions.add(node.name)
        self.generic_visit(node)

    def visit_Call(self, node: Call):
        self.stats.func_calls.add(self.get_name(node.func))
        self.generic_visit(node)

    def visit_Assign(self, node: Assign):
        for target in node.targets:
            name = self.get_name(target)
            logger.info(f'assign: {name} {node.value}')
            self.stats.assignments.add(name)
        self.generic_visit(node)

    def visit_Tuple(self, node: Tuple) -> Any:
        logger.warning(f'tuple: not implemented yet: [{self.get_name(node)}]')

    def visit_Subscript(self, node: Subscript) -> Any:
        logger.info(f'subscript: {node}')
        self.generic_visit(node)

    def visit_Constant(self, node: Constant) -> Any:
        self.stats.constants.add(self.get_name(node))

    def get_name(self, item: Any):
        match item:
            case Tuple():
                x = ','.join([self.get_name(_) for _ in item.elts])
                return f'({x})'
            case Subscript():
                return self.get_name(item.value)
            case Call():
                return self.get_name(item.func)
            case Name():
                return item.id
            case Attribute():
                return f'{self.get_name(item.value)}.{item.attr}'
            case Constant():
                return self.get_name(item.value)
            case List():
                x = ','.join([self.get_name(_) for _ in item.elts])
                return f'[{x}]'
            case BinOp():
                return f'{item.op}[{self.get_name(item.left)} {self.get_name(item.right)}]'
            case UnaryOp():
                return f'{item.op}[{self.get_name(item.operand)}]'
            case Lambda():
                return f'Lambda[{item}]'
            # case ellipsis():
            #     return str(item)
            case str():
                return item
            case int():
                return str(item)
            case float():
                return str(item)
            case bool():
                return str(item)
            case None:
                return 'None'
            case _:
                logger.warning(f'unhandled type: {type(item)}')
                return str(item)
