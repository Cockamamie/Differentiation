from re import findall
from differentiation import *
import queue

operators = ['+', '-', '*', '/', '^']
funcs = ['sin', 'cos', 'tan', 'cot', 'log']


def parse(expression):
    expression = simplify(expression)
    split_expression = split(expression)
    prefix_expression = to_prefix(split_expression)
    print(prefix_expression)
    root = to_tree(prefix_expression)
    return root


def simplify(expression):
    expression = expression.replace(' ', '')
    # TODO remove redundant brackets
    # TODO replace ln(x) and lg(x) with log(e,x) and log(10, x)
    return expression


def split(expression):
    pattern = r'\d+|x|\+|\-|\*|\/|\^|sin|cos|tan|cot|log|\(|\)'
    return findall(pattern, expression)


def is_const_or_param(s): return s.isdigit() or s == 'x'


def is_operator_or_func(s):
    return s in operators or s in funcs


def to_prefix(expression):
    priority = {'(': 0, ')': 0,
                '+': 1, '-': 1,
                '*': 2, '/': 2,
                'sin': 2, 'cos': 2,
                'tan': 2, 'cot': 2,
                'log': 2,
                '^': 3}
    q = queue.Queue()
    stack = []
    for element in expression:
        if is_const_or_param(element):
            q.put(element)
        if is_operator_or_func(element):
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
        if is_unary(element):
            arg = stack.pop()
            stack.append(class_by_name[element](arg))
        if is_binary(element):
            right = stack.pop()
            left = stack.pop()
            stack.append(class_by_name[element](left, right))
    return stack[0]
