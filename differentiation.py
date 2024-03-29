from sympy import E, simplify
from interfaces import Dx, Binary, Unary
import sys


def invalid_expression(message='Invalid expression'):
    print(f'Error: {message}')
    sys.exit(1)


def differentiate(root): return simplify(str(root.dx()))


def negate(arg: Dx): return Multiply(Const(-1), arg)


class Const(Dx):
    def __init__(self, value: float):
        self.value = value

    def dx(self):
        return Const(0)

    def __str__(self):
        return f'{self.value}'


class X(Dx):
    def dx(self):
        return Const(1)

    def __str__(self):
        return 'x'


class Append(Dx, Binary):
    def __init__(self, left: Dx, right: Dx):
        self.left = left
        self.right = right

    def __str__(self):
        return f'({self.left}+{self.right})'

    def dx(self):
        left_operand = self.left.dx()
        right_operand = self.right.dx()
        return Append(left_operand, right_operand)


class Subtract(Dx, Binary):
    def __init__(self, left: Dx, right: Dx):
        self.left = left
        self.right = right

    def __str__(self):
        return f'({self.left} - {self.right})'

    def dx(self):
        left_operand = self.left.dx()
        right_operand = self.right.dx()
        return Subtract(left_operand, right_operand)


class Multiply(Dx, Binary):
    def __init__(self, left: Dx, right: Dx):
        self.left = left
        self.right = right

    def __str__(self):
        return f'({self.left} * {self.right})'

    def dx(self):
        left_derivative = self.left.dx()
        right_derivative = self.right.dx()
        left_operand = Multiply(left_derivative, self.right)
        right_operand = Multiply(self.left, right_derivative)
        return Append(left_operand, right_operand)


class Divide(Dx, Binary):
    def __init__(self, numerator: Dx, denominator: Dx):
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self):
        return f'(({self.numerator}) / ({self.denominator}))'

    def dx(self):
        numerator_derivative = self.numerator.dx()
        denominator_derivative = self.denominator.dx()
        numerator_left_operand = Multiply(numerator_derivative, self.denominator)
        numerator_right_operand = Multiply(self.numerator, denominator_derivative)
        numerator = Subtract(numerator_left_operand, numerator_right_operand)
        denominator = Multiply(self.denominator, self.denominator)
        return Divide(numerator, denominator)


class Power(Dx, Binary):
    def __init__(self, base: Dx, exponent: Dx):
        self.base = base
        self.exponent = exponent

    def dx(self):
        left = Multiply(Multiply(self.exponent, Power(self.base, Subtract(self.exponent, Const(1)))), self.base.dx())
        right = Multiply(Power(self.base, self.exponent), Multiply(Log(E, self.base), self.exponent.dx()))
        return Append(left, right)

    def __str__(self):
        return f'(({self.base})^({self.exponent}))'


class Sin(Dx, Unary):
    def __init__(self, arg: Dx):
        self.arg = arg

    def dx(self):
        return Multiply(Cos(self.arg), self.arg.dx())

    def __str__(self):
        return f'sin({self.arg})'


class Cos(Dx, Unary):
    def __init__(self, arg: Dx):
        self.arg = arg

    def dx(self):
        return Multiply(negate(Sin(self.arg)), self.arg.dx())

    def __str__(self):
        return f'cos({self.arg})'


class Tan(Dx, Unary):
    def __init__(self, arg: Dx):
        self.arg = arg

    def dx(self):
        tg_derivative_denominator = Multiply(Cos(self.arg), Cos(self.arg))
        tg_derivative = Divide(Const(1), tg_derivative_denominator)
        return Multiply(tg_derivative, self.arg.dx())

    def __str__(self):
        return f'tan({self.arg})'


class Cot(Dx, Unary):
    def __init__(self, arg: Dx):
        self.arg = arg

    def dx(self):
        ctg_derivative_denominator = Multiply(Sin(self.arg), Sin(self.arg))
        ctg_derivative = Divide(Const(1), ctg_derivative_denominator)
        return Multiply(negate(ctg_derivative), self.arg.dx())

    def __str__(self):
        return f'cot({self.arg})'


class Log(Dx, Binary):
    def __init__(self, base: Dx, arg: Dx):
        if isinstance(base, Const) and (base.value == 1 or base.value <= 0):
            invalid_expression('Logarithm base must be greater than zero and not equal to one')
        if isinstance(arg, Const) and arg.value <= 0:
            invalid_expression('Logarithm argument must be greater than zero')
        self.base = base
        self.arg = arg

    def __str__(self):
        return f'log({self.base},{self.arg})'

    @staticmethod
    def extract_degree(arg):
        if isinstance(arg, Power):
            return Multiply(arg.exponent, Log(Const(2), arg.base))
        return Log(Const(2), arg)

    def dx(self):
        if isinstance(self.base, Const):
            denominator = Multiply(self.arg, Log(Const(E), self.base))
            left = self.arg.dx()
            right = Divide(Const(1), denominator)
            return Multiply(left, right)
        numerator = self.extract_degree(self.arg)
        denominator = self.extract_degree(self.base)
        return Divide(numerator, denominator).dx()
