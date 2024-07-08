from __future__ import annotations
from sympy import Expr, parse_expr, expand, Add, Mul, Pow
from typing import TYPE_CHECKING
from icecream import ic

if TYPE_CHECKING:
    from expressionism.graph import ExpressionGraph


class Node:
    def __init__(self, id: str, type: str, data: dict):
        self.id = id
        self.type = type
        self.data = data
        self.inputs: list[str] = []

    def calc(self, graph: ExpressionGraph) -> Expr:
        pass

    def __repr__(self) -> str:
        return f"Node({self.id}, {self.type}, {self.data}, {self.inputs})"


class FixedNode(Node):
    def __init__(self, id: str, type: str, data: dict):
        super().__init__(id, type, data)
        self.result: Expr | None = None


class ResultNode(Node):
    def __init__(self, id: str, data: dict):
        super().__init__(id, "result", data)

    def calc(self, graph: ExpressionGraph) -> Expr:
        expr_node = graph.get_linked_node(self.id, "inp-1")
        if expr_node is None:
            raise ValueError("No linked node for result found")

        return expr_node.calc(graph)


class ExpressionNode(FixedNode):
    def __init__(self, id: str, data: dict):
        super().__init__(id, "expression", data)

    def calc(self, graph: ExpressionGraph) -> Expr:
        if self.result is None:
            self.result = parse_expr(self.data["value"], evaluate=False)
        return self.result


class JoinNode(Node):
    def __init__(self, id: str, data: dict):
        super().__init__(id, "join", data)

    def calc(self, graph: ExpressionGraph) -> Expr:
        operator = self.data["operator"]

        expr_1_node = graph.get_linked_node(self.id, "expression-1")
        if expr_1_node is None:
            raise ValueError("No linked node for expression 1 found")

        expr_2_node = graph.get_linked_node(self.id, "expression-2")
        if expr_2_node is None:
            raise ValueError("No linked node for expression 2 found")

        expr_1: Expr = expr_1_node.calc(graph)
        expr_2: Expr = expr_2_node.calc(graph)

        if operator == "+":
            return Add(expr_1, expr_2, evaluate=False)
        elif operator == "-":
            return Add(expr_1, -1 * expr_2, evaluate=False)
        elif operator == "*":
            return Mul(expr_1, expr_2, evaluate=False)
        elif operator == "/":
            return Mul(expr_1, Pow(expr_2, -1, evaluate=False), evaluate=False)
        else:
            raise ValueError(f"Unknown operator: {operator}")


def create_node_from_type(node_type: str, id: str, data: dict) -> Node:
    if node_type == "expression":
        return ExpressionNode(id, data)
    elif node_type == "join":
        return JoinNode(id, data)
    elif node_type == "result":
        return ResultNode(id, data)
    else:
        # TODO remove that in the future
        return Node(id, node_type, data)
    # elif node_type == "merge":
    #     return MergeNode(id, data)
    # elif node_type == "branch":
    #     return BranchNode(id, data)
    # elif node_type == "branch_group":
    #     return BranchGroupNode(id, data)
    # else:
    #     raise ValueError(f"Unknown node type: {node_type}")
    pass
