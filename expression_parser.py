import sys
from re import findall
from differentiation import *
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


def invalid_expression():
    print('Error: Invalid expression')
    sys.exit(1)


def parse(expression):
    split_expr = split_expression(expression)
    bracketed = place_func_arg_brackets(split_expr)
    multiplied = place_multi_sign(bracketed)
    prefix_expression = to_prefix(multiplied)
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
    return expression


def split(expression):
    pattern = r'\d+|E|pi|x|\+|\-|\*|\/|\^|sin|cos|tan|cot|\(|\)'
    return findall(pattern, expression)


def split_expression(expression):
    simplified = simplify(expression.lower()).replace('e', 'E')
    split_expr = split(simplified)
    reminder = simplified
    for e in split_expr:
        reminder = reminder.replace(e, '')
    if len(reminder) > 0:
        invalid_expression()
    return split_expr


def get_args_len(bracketed):
    length = 0
    current = bracketed[0]
    while (is_const_or_param(current) or PRIORITY[current] > PRIORITY['+']) and not is_func(current):
        length += 1
        if length >= len(bracketed):
            break
        current = bracketed[length]
    print(f'{length = }')
    return length


def place_func_arg_brackets(split_expr):
    bracketed = list(split_expr)
    i = 0
    length = len(bracketed)
    while i < length:
        print(f'{bracketed = }')
        current = bracketed[i]
        if is_func(current) and bracketed[i + 1] != '(':
            bracketed.insert(i + 1, '(')
            if is_unary(current):
                right_parenthesis_index = i + 1 + get_args_len(bracketed[i + 2:]) + 1
                bracketed.insert(right_parenthesis_index, ')')
                length = len(bracketed)
                i += 1
                continue
        i += 1
    return bracketed


def place_multi_sign(split_expr):
    multiplied = list(split_expr)
    length = len(multiplied)
    index = 1
    while index < length:
        current = multiplied[index]
        previous = multiplied[index - 1]
        previous_condition = previous == ')' or is_param(previous) or is_const(previous)
        current_condition = current == '(' or (not is_operator(current) and current != ')')
        if previous_condition and current_condition:
            multiplied.insert(index, '*')
            index += 2
            length = len(multiplied)
            continue
        index += 1
    return multiplied


def to_prefix(expression):
    q = Queue()
    stack = []
    for element in expression:
        if is_const_or_param(element):
            q.put(element)
        if is_func(element):
            stack.append(element)
        if is_operator(element):
            if not stack or stack[-1] == '(':
                stack.append(element)
                continue
            if PRIORITY[element] > PRIORITY[stack[-1]]:
                stack.append(element)
                continue
            if PRIORITY[element] <= PRIORITY[stack[-1]]:
                while stack and stack[-1] != '(' and PRIORITY[element] < PRIORITY[stack[-1]]:
                    q.put(stack.pop())
                stack.append(element)
        if element == '(':
            stack.append(element)
        if element == ')':
            if '(' not in stack:
                invalid_expression()
            while stack[-1] != '(':
                q.put(stack.pop())
            stack.pop()
    if ')' in stack or '(' in stack:
        invalid_expression()
    while stack:
        q.put(stack.pop())
    res = []
    while not q.empty():
        res.append(q.get())
    return res


def is_binary(operator):
    return operator in OPERATORS


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
        invalid_expression()
    return stack[0]
