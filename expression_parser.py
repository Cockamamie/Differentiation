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


def invalid_expression(message):
    print(f'Error: Invalid expression\n{" " * 7}{message}')
    sys.exit(1)


def parse(expression):
    try:
        split_expr = split_expression(expression)
        bracketed = place_func_arg_brackets(split_expr)
        multiplied = place_multi_sign(bracketed)
        prefix_expression = to_prefix(multiplied)
        root = to_tree(prefix_expression)
        return root
    except IndexError:
        invalid_expression("If you put spaces between characters in the expression, enclose it in brackets.\n"
                           f"{' ' * 7}Use ^ for exponentiation instead of **.\n"
                           f"{' ' * 7}Unary arithmetic operators aren't supported.\n"
                           f"{' ' * 7}If you want to use log(x) as natural logarithm enter ln(x) instead.")


def is_num(s): return len(findall(r'\d*\.\d+|\d+', s)) > 0


def is_const(s): return is_num(s) or s in ['pi', 'E']


def is_param(s): return s == 'x'


def is_func(s): return s in FUNCS


def is_operator(s): return s in OPERATORS


def is_const_or_param(s): return is_const(s) or is_param(s)


def is_operator_or_func(s): return is_operator(s) or is_func(s)


def insert(expression, index, symbol):
    return expression[:index] + symbol + expression[index:]


def place_ln_lg_brackets(expression):
    in_brackets = [str(i) for i in range(0, 10)] + ['x', '*', '^', '/']
    for i, symbol in enumerate(expression[:len(expression) - 1]):
        log_challenger = symbol + expression[i + 1]
        if (log_challenger == 'ln' or log_challenger == 'lg') and expression[i + 2] != '(':
            expression = insert(expression, i + 2, '(')
            index = i + 2
            while expression[index] in in_brackets:
                index += 1
                if index >= len(expression):
                    break
            expression = insert(expression, index + 2, ')')


def place_log_args_brackets(expression):
    for i in range(len(expression) - 3):
        log_challenger = expression[i] + expression[i + 1] + expression[i + 2]
        if log_challenger == 'log':
            expression = insert(expression, i + 4, '(')
            brackets_count = 1
            index = i + 5
            while brackets_count > 0:
                if expression[index] == '(':
                    brackets_count += 1
                if expression[index] == ')':
                    brackets_count -= 1
                if expression[index] == ',':
                    expression = insert(expression, index, ')')
                    expression = insert(expression, index + 2, '(')
                    index += 3
                index += 1
            expression = insert(expression, index, ')')
    return expression


def simplify(expression):
    expression = expression.replace(' ', '')
    place_ln_lg_brackets(expression)
    expression = expression.replace('ln(', 'log(e,')
    expression = expression.replace('lg(', 'log(10,')
    expression = place_log_args_brackets(expression)
    return expression


def split(expression):
    pattern = r'\d*\.\d+|\d+|E|pi|x|\+|\-|\*|\/|\^|sin|cos|tan|cot|log|\(|\)|,|\.'
    return findall(pattern, expression)


def split_expression(expression):
    simplified = simplify(expression.lower()).replace('e', 'E')
    split_expr = split(simplified)
    reminder = simplified
    logs_count = simplified.count('log')
    commas_count = simplified.count(',')
    float_count = len(findall(r"d*\.\d+", expression))
    dots_count = simplified.count('.')
    if float_count < dots_count:
        invalid_expression(f'Invalid symbol " . "')
    if logs_count < commas_count:
        invalid_expression(f'Invalid symbol " , "')
    for e in split_expr:
        reminder = reminder.replace(e, '')
    if len(reminder) - logs_count > 0:
        invalid_expression(f'Invalid symbol " {reminder[0]} "')
    return split_expr


def get_args_len(bracketed):
    length = 0
    current = bracketed[0]
    while (is_const_or_param(current) or PRIORITY[current] > PRIORITY['+']) and not is_func(current):
        length += 1
        if length >= len(bracketed):
            break
        current = bracketed[length]
    return length


def place_func_arg_brackets(split_expr):
    bracketed = list(split_expr)
    i = 0
    length = len(bracketed)
    while i < length:
        current = bracketed[i]
        if is_func(current) and is_unary(current) and bracketed[i + 1] != '(':
            bracketed.insert(i + 1, '(')
            right_parenthesis_index = i + 1 + get_args_len(bracketed[i + 2:]) + 1
            bracketed.insert(right_parenthesis_index, ')')
            length = len(bracketed)
            i += 1
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
        if previous_condition and current_condition and previous != ',' and current != ',':
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
                invalid_expression('Misplaced brackets')
            while stack[-1] != '(':
                q.put(stack.pop())
            stack.pop()
    if ')' in stack or '(' in stack:
        invalid_expression('Misplaced brackets')
    while stack:
        q.put(stack.pop())
    res = []
    while not q.empty():
        res.append(q.get())
    return res


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
                if is_num(element):
                    if element.isdigit():
                        stack.append(Const(int(element)))
                    else:
                        stack.append(Const(float(element)))
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
        invalid_expression(f'Invalid expression with symbol {stack[1]}')
    return stack[0]
