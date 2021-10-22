import unittest
from differentiation import *
from sympy import *
from expression_parser import parse


class Test(unittest.TestCase):
    def assert_dx_equal(self, func, to_dif: Dx):
        d = to_dif.dx()
        print(f'expr before simplify = {str(d)}')
        expr = simplify(str(d))
        print(f'expr after simplify = {expr}')
        func = simplify(str(func))
        print(f'{expr}, {func}')
        if expr == 0:
            self.assertEqual(0, func)
            return
        self.assertEqual(1, func / expr)


class TestConstAndParam(unittest.TestCase):
    def test_const(self):
        func = Const(0)
        to_dif = Const(5)
        Test().assert_dx_equal(func, to_dif)

    def test_param(self):
        func = Const(1)
        to_dif = X()
        Test().assert_dx_equal(func, to_dif)


class TestAddition(unittest.TestCase):
    def test_const_const(self):
        func = Const(0)
        to_dif = Append(Const(5), Const(1))
        Test().assert_dx_equal(func, to_dif)

    def test_const_param(self):
        func = Const(1)
        to_dif = Append(Const(2), X())
        Test().assert_dx_equal(func, to_dif)

    def test_param_param(self):
        func = Const(2)
        to_dif = Append(X(), X())
        Test().assert_dx_equal(func, to_dif)


class TestSubtraction(unittest.TestCase):
    def test_const_const(self):
        func = Const(0)
        to_dif = Subtract(Const(5), Const(1))
        Test().assert_dx_equal(func, to_dif)

    def test_const_param(self):
        func = Const(-1)
        to_dif = Subtract(Const(2), X())
        Test().assert_dx_equal(func, to_dif)

    def test_param_param(self):
        func = Const(0)
        to_dif = Subtract(X(), X())
        Test().assert_dx_equal(func, to_dif)


class TestMultiplication(unittest.TestCase):
    def test_const_const(self):
        func = Const(0)
        to_dif = Multiply(Const(5), Const(2))
        Test().assert_dx_equal(func, to_dif)

    def test_const_param(self):
        func = Const(5)
        to_dif = Multiply(Const(5), X())
        Test().assert_dx_equal(func, to_dif)

    def test_param_param(self):
        func = Multiply(Const(2), X())
        to_dif = Multiply(X(), X())
        Test().assert_dx_equal(func, to_dif)


class TestDivision(unittest.TestCase):
    def test_const_const(self):
        func = Const(0)
        to_dif = Divide(Const(5), Const(2))
        Test().assert_dx_equal(func, to_dif)

    def test_const_param(self):
        func = Divide(Const(-5), Power(X(), Const(2)))
        to_dif = Divide(Const(5), X())
        Test().assert_dx_equal(func, to_dif)

    def test_param_param(self):
        func = Const(0)
        to_dif = Divide(X(), X())
        Test().assert_dx_equal(func, to_dif)


class TestTrigonometry(unittest.TestCase):
    def test_sin_const(self):
        func = Const(0)
        to_dif = Sin(Const(5))
        Test().assert_dx_equal(func, to_dif)

    def test_sin_param(self):
        func = Cos(X())
        to_dif = Sin(X())
        Test().assert_dx_equal(func, to_dif)

    def test_cos_const(self):
        func = Const(0)
        to_dif = Cos(Const(5))
        Test().assert_dx_equal(func, to_dif)

    def test_cos_param(self):
        func = Multiply(Const(-1), Sin(X()))
        to_dif = Cos(X())
        Test().assert_dx_equal(func, to_dif)

    def test_tan_const(self):
        func = Const(0)
        to_dif = Tan(Const(5))
        Test().assert_dx_equal(func, to_dif)

    def test_tan_param(self):
        func = Divide(Const(1), Power(Cos(X()), Const(2)))
        to_dif = Tan(X())
        Test().assert_dx_equal(func, to_dif)

    def test_cot_const(self):
        func = Const(0)
        to_dif = Cot(Const(5))
        Test().assert_dx_equal(func, to_dif)

    def test_cot_param(self):
        func = Divide(Const(-1), Power(Sin(X()), Const(2)))
        to_dif = Cot(X())
        Test().assert_dx_equal(func, to_dif)


class TestLogarithm(unittest.TestCase):
    def test_const_const(self):
        func = Const(0)
        to_dif = Log(Const(2), Const(5))
        Test().assert_dx_equal(func, to_dif)

    def test_const_param(self):
        func = Divide(Const(1), Multiply(Log(E, Const(2)), X()))
        to_dif = Log(Const(2), X())
        Test().assert_dx_equal(func, to_dif)

    def test_param_const(self):
        func = negate(Divide(Log(E, Const(2)), Multiply(X(), Power(Log(E, X()), Const(2)))))
        to_dif = Log(X(), Const(2))
        Test().assert_dx_equal(func, to_dif)

    def test_param_param(self):
        func = Const(0)
        to_dif = Log(X(), X())
        Test().assert_dx_equal(func, to_dif)

    def test_param_param_func_func(self):
        func = Const(0)
        to_dif = Log(Power(X(), Const(2)), Power(X(), Const(3)))
        Test().assert_dx_equal(func, to_dif)


class TestPower(unittest.TestCase):
    def test_const_const(self):
        func = Const(0)
        to_dif = Power(Const(5), Const(2))
        Test().assert_dx_equal(func, to_dif)

    def test_const_const_rational_exp(self):
        func = Const(0)
        to_dif = Power(Const(5), Const(1 / 2))
        Test().assert_dx_equal(func, to_dif)

    def test_param_const(self):
        func = Multiply(Const(7), Power(X(), Const(6)))
        to_dif = Power(X(), Const(7))
        Test().assert_dx_equal(func, to_dif)

    def test_param_const_rational_exp(self):
        func = Divide(Const(1), Multiply(Const(2), Power(X(), Const(1 / 2))))
        to_dif = Power(X(), Const(1 / 2))
        Test().assert_dx_equal(func, to_dif)


def replace_all(expressions, to_replace, replacer):
    return [expr.replace(to_replace, replacer) for expr in expressions]


class TestParser(unittest.TestCase):
    def assert_parsed_equals_expr(self, expr):
        parsed = parse(expr)
        self.assertEqual(sympify(expr), simplify(str(parsed)))

    def test_const(self):
        expression = '2'
        self.assert_parsed_equals_expr(expression)

    def test_param(self):
        expression = 'x'
        self.assert_parsed_equals_expr(expression)

    const_expressions = ['1~2', '1 ~ 2', '(1~2)', '(1) ~ (2)']
    param_const_expressions = ['x~2', 'x ~ 2', '(x~2)', '(x) ~ (2)']
    param_param_expressions = ['x~x', 'x ~ x', '(x~x)', '(x) ~ (x)']

    def assert_expressions(self, expressions):
        for expression in expressions:
            expr = expression
            self.assert_parsed_equals_expr(expr)

    def test_add_consts(self):
        self.assert_expressions(replace_all(self.const_expressions, '~', '+'))

    def test_subtract_consts(self):
        self.assert_expressions(replace_all(self.const_expressions, '~', '-'))

    def test_multiply_consts(self):
        self.assert_expressions(replace_all(self.const_expressions, '~', '*'))

    def test_divide_consts(self):
        self.assert_expressions(replace_all(self.const_expressions, '~', '/'))

    def test_add_params(self):
        self.assert_expressions(replace_all(self.param_const_expressions, '~', '+'))
        self.assert_expressions(replace_all(self.param_param_expressions, '~', '+'))

    def test_subtract_params(self):
        self.assert_expressions(replace_all(self.param_const_expressions, '~', '-'))
        self.assert_expressions(replace_all(self.param_param_expressions, '~', '-'))

    def test_multiply_params(self):
        self.assert_expressions(replace_all(self.param_const_expressions, '~', '*'))
        self.assert_expressions(replace_all(self.param_param_expressions, '~', '*'))

    def test_divide_params(self):
        self.assert_expressions(replace_all(self.param_const_expressions, '~', '/'))
        self.assert_expressions(replace_all(self.param_param_expressions, '~', '/'))


if __name__ == '__main__':
    unittest.main()
