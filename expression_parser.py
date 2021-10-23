from re import findall
from differentiation import *
import queue
from queue import Queue
from sympy import E, pi

OPERATORS = ['+', '-', '*', '/', '^']
FUNCS = ['sin', 'cos', 'tan', 'cot', 'log']
PRIORITY = {'(': 0, ')': 0,
            '+': 1, '-': 1,
            '*': 2, '/': 2,
            '^': 3,
            'sin': 4, 'cos': 4,
            'tan': 4, 'cot': 4,
            'log': 4}

operators = ['+', '-', '*', '/', '^']
funcs = ['sin', 'cos', 'tan', 'cot', 'log']

class InvalidExpressionError(Exception):
    pass


def parse(expression):
    expression = simplify(expression)
    split_expression = split(expression)
    prefix_expression = to_prefix(split_expression)
    print(prefix_expression)
    split_expr = split_expression(expression)
    prefix_expression = to_prefix(split_expr)
    root = to_tree(prefix_expression)
    return root


def is_const(s): return s.isdigit() or s in ['pi', 'E']


def is_param(s): return s == 'x'


def is_func(s): return s in FUNCS


def is_operator(s): return s in OPERATORS


def is_const_or_param(s): return is_const(s) or is_param(s)


def is_operator_or_func(s): return is_operator(s) or is_func(s)


def simplify(expression):
    expression = expression.replace(' ', '')
    # TODO remove redundant brackets
    # TODO replace ln(x) and lg(x) with log(e,x) and log(10, x)
    expression = expression.replace('ln(', 'log(e,')
    expression = expression.replace('lg(', 'log(10,')
    return expression


def split(expression):
    pattern = r'\d+|x|\+|\-|\*|\/|\^|sin|cos|tan|cot|log|\(|\)'
    pattern = r'\d+|E|pi|x|\+|\-|\*|\/|\^|sin|cos|tan|cot|log|\(|\)'
    return findall(pattern, expression)


def is_const_or_param(s): return s.isdigit() or s == 'x'


def is_operator_or_func(s):
    return s in operators or s in funcs
def split_expression(expression):
    simplified = simplify(expression.lower()).replace('e', 'E')
    split_expr = split(simplified)
    reminder = simplified
    for e in split_expr:
        reminder = reminder.replace(e, '')
    if len(reminder) > 0:
        raise InvalidExpressionError
    return split_expr


def to_prefix(expression):
    priority = {'(': 0, ')': 0,
                '+': 1, '-': 1,
                '*': 2, '/': 2,
                'sin': 2, 'cos': 2,
                'tan': 2, 'cot': 2,
                'log': 2,
                '^': 3}
    q = queue.Queue()
    q = Queue()
    stack = []
    for element in expression:
        if is_const_or_param(element):
            q.put(element)
            if not stack or stack[-1] == '(':
                stack.append(element)
            elif priority[element] > priority[stack[-1]]:
                stack.append(element)
            elif priority[element] <= priority[stack[-1]]:
                while priority[element] <= priority[stack[-1]] or stack[-1] != '(':
                    q.put(stack.pop())
                stack.append(element)
        if element == '(':
            stack.append(element)
        if element == ')':
            while stack[-1] != '(':
                q.put(stack.pop())
            stack.pop()
    while stack:
        q.put(stack.pop())
    res = []
    while not q.empty():
        res.append(q.get())
    return res


def is_binary(operator):
    return operator in operators + ['log']


def is_unary(operator):
    return operator in funcs[:len(funcs) - 1]
def to_tree(prefix_expr):
    def is_binary(operator):
        return operator in OPERATORS + ['log']

    def is_unary(operator):
        return operator in FUNCS[:len(FUNCS) - 1]

def to_tree(prefix_expr):
    class_by_name = {'+': Append, '-': Subtract,
                     '*': Multiply, '/': Divide,
                     'sin': Sin, 'cos': Cos,
                     'tan': Tan, 'cot': Cot,
                     'log': Log, '^': Power}
    stack = []
    for element in prefix_expr:
        if is_const_or_param(element):
            if element == 'x':
                stack.append(X())
            else:
                stack.append(Const(int(element)))
                if element.isdigit():
                    stack.append(Const(int(element)))
                if element == 'E':
                    stack.append(Const(E))
                if element == 'pi':
                    stack.append(Const(pi))
        if is_unary(element):
            arg = stack.pop()
            stack.append(class_by_name[element](arg))
        if is_binary(element):
            right = stack.pop()
            left = stack.pop()
            stack.append(class_by_name[element](left, right))
    if len(stack) > 1:
        raise InvalidExpressionError
    return stack[0]
