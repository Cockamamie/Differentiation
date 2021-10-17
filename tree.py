from enum import Enum


class NodeType(Enum):
    operand = 1
    operator = 2


class Node:
    def __init__(self, node_type, value,
                 parent=None, left=None, right=None):
        self.node_type = node_type
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right

