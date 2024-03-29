import unittest
from differentiation import *
from sympy import *
from expression_parser import parse


class Test(unittest.TestCase):
    def assert_dx_equal(self, derivative, to_dif: Dx):
        d = to_dif.dx()
        expr = simplify(str(d))
        derivative = simplify(str(derivative))
        if expr == 0:
            self.assertEqual(0, derivative)
            return
        self.assertEqual(1, derivative / expr)


class TestConstAndParam(unittest.TestCase):
    def test_const(self):
        to_dif = Const(5)
        derivative = Const(0)
        Test().assert_dx_equal(derivative, to_dif)

    def test_param(self):
        to_dif = X()
        derivative = Const(1)
        Test().assert_dx_equal(derivative, to_dif)


class TestAddition(unittest.TestCase):
    def test_const_const(self):
        to_dif = Append(Const(5), Const(1))
        derivative = Const(0)
        Test().assert_dx_equal(derivative, to_dif)

    def test_const_param(self):
        to_dif = Append(Const(2), X())
        derivative = Const(1)
        Test().assert_dx_equal(derivative, to_dif)

    def test_param_param(self):
        to_dif = Append(X(), X())
        derivative = Const(2)
        Test().assert_dx_equal(derivative, to_dif)


class TestSubtraction(unittest.TestCase):
    def test_const_const(self):
        to_dif = Subtract(Const(5), Const(1))
        derivative = Const(0)
        Test().assert_dx_equal(derivative, to_dif)

    def test_const_param(self):
        to_dif = Subtract(Const(2), X())
        derivative = Const(-1)
        Test().assert_dx_equal(derivative, to_dif)

    def test_param_param(self):
        to_dif = Subtract(X(), X())
        derivative = Const(0)
        Test().assert_dx_equal(derivative, to_dif)

    def test_param_param_expression(self):
        to_dif = Subtract(Sin(Power(Const(2), X())), Log(Const(E), Power(X(), Const(2))))
        derivative = Subtract(
            Multiply(
                Power(Const(2), X()),
                Multiply(Log(E, Const(2)), Cos(Power(Const(2), X())))),
            Divide(Const(2), X()))
        Test().assert_dx_equal(derivative, to_dif)


class TestMultiplication(unittest.TestCase):
    def test_const_const(self):
        to_dif = Multiply(Const(5), Const(2))
        derivative = Const(0)
        Test().assert_dx_equal(derivative, to_dif)

    def test_const_param(self):
        to_dif = Multiply(Const(5), X())
        derivative = Const(5)
        Test().assert_dx_equal(derivative, to_dif)

    def test_param_param(self):
        to_dif = Multiply(X(), X())
        derivative = Multiply(Const(2), X())
        Test().assert_dx_equal(derivative, to_dif)

    def test_param_param_expression(self):
        to_dif = Multiply(Power(Const(2), Multiply(Const(3), X())), Log(Const(E), X()))
        derivative = Append(
            Multiply(
                Multiply(Const(3), Power(Const(8), X())),
                Multiply(Log(E, Const(2)), Log(E, X()))),
            Divide(Power(Const(8), X()), X()))
        Test().assert_dx_equal(derivative, to_dif)


class TestDivision(unittest.TestCase):
    def test_const_const(self):
        to_dif = Divide(Const(5), Const(2))
        derivative = Const(0)
        Test().assert_dx_equal(derivative, to_dif)

    def test_const_param(self):
        to_dif = Divide(Const(5), X())
        derivative = Divide(Const(-5), Power(X(), Const(2)))
        Test().assert_dx_equal(derivative, to_dif)

    def test_param_param(self):
        to_dif = Divide(X(), X())
        derivative = Const(0)
        Test().assert_dx_equal(derivative, to_dif)

    def test_param_param_expression(self):
        to_dif = Divide(Sin(Append(X(), Const(3))), X())
        derivative = Divide(
            Subtract(
                Multiply(Cos(Append(X(), Const(3))), X()),
                Sin(Append(X(), Const(3)))),
            Power(X(), Const(2)))
        Test().assert_dx_equal(derivative, to_dif)


class TestTrigonometry(unittest.TestCase):
    def test_sin_const(self):
        to_dif = Sin(Const(5))
        derivative = Const(0)
        Test().assert_dx_equal(derivative, to_dif)

    def test_sin_param(self):
        to_dif = Sin(X())
        derivative = Cos(X())
        Test().assert_dx_equal(derivative, to_dif)

    def test_sin_param_expression(self):
        to_dif = Sin(Append(Power(X(), Const(2)), Sin(Const(9))))
        derivative = Multiply(
            Multiply(Const(2), X()),
            Cos(Append(Power(X(), Const(2)), Sin(Const(9)))))
        Test().assert_dx_equal(derivative, to_dif)

    def test_cos_const(self):
        to_dif = Cos(Const(5))
        derivative = Const(0)
        Test().assert_dx_equal(derivative, to_dif)

    def test_cos_param(self):
        to_dif = Cos(X())
        derivative = Multiply(Const(-1), Sin(X()))
        Test().assert_dx_equal(derivative, to_dif)

    def test_cos_param_expression(self):
        to_dif = Power(Cos(Divide(Multiply(Const(7), X()), Cos(Const(4)))), Const(2))
        derivative = negate(Divide(
            Multiply(Const(7),
                     Sin(Divide(
                         Multiply(Const(14), X()), Cos(Const(4))))),
            Cos(Const(4))))
        Test().assert_dx_equal(derivative, to_dif)

    def test_tan_const(self):
        to_dif = Tan(Const(5))
        derivative = Const(0)
        Test().assert_dx_equal(derivative, to_dif)

    def test_tan_param(self):
        to_dif = Tan(X())
        derivative = Divide(Const(1), Power(Cos(X()), Const(2)))
        Test().assert_dx_equal(derivative, to_dif)

    def test_tan_param_expression(self):
        to_dif = Tan(Power(Multiply(Const(2), Const(3)), X()))
        derivative = Multiply(Power(Const(6), X()),
                              Multiply(
                                  Log(Const(E), Const(6)),
                                  Power(Divide(Const(1), Cos(Power(Const(6), X()))),
                                        Const(2))))
        Test().assert_dx_equal(derivative, to_dif)

    def test_cot_const(self):
        to_dif = Cot(Const(5))
        derivative = Const(0)
        Test().assert_dx_equal(derivative, to_dif)

    def test_cot_param(self):
        to_dif = Cot(X())
        derivative = Divide(Const(-1), Power(Sin(X()), Const(2)))
        Test().assert_dx_equal(derivative, to_dif)

    def test_cot_param_expression(self):
        to_dif = Cot(Cot(Power(X(), Const(2))))
        derivative = Multiply(
            Multiply(X(), Power(Sin(Cot(Power(X(), Const(2)))), Const(-2))),
            Multiply(Const(2), Power(Sin(Power(X(), Const(2))), Const(-2))))
        Test().assert_dx_equal(derivative, to_dif)


class TestLogarithm(unittest.TestCase):
    def test_const_const(self):
        to_dif = Log(Const(2), Const(5))
        derivative = Const(0)
        Test().assert_dx_equal(derivative, to_dif)

    def test_const_param(self):
        to_dif = Log(Const(2), X())
        derivative = Divide(Const(1), Multiply(Log(E, Const(2)), X()))
        Test().assert_dx_equal(derivative, to_dif)

    def test_param_const(self):
        to_dif = Log(X(), Const(2))
        derivative = negate(Divide(
            Log(E, Const(2)),
            Multiply(X(), Power(Log(E, X()), Const(2)))))
        Test().assert_dx_equal(derivative, to_dif)

    def test_param_param(self):
        to_dif = Log(X(), X())
        derivative = Const(0)
        Test().assert_dx_equal(derivative, to_dif)

    def test_param_expression_param_expression(self):
        to_dif = Log(Power(X(), Const(2)), Power(X(), Const(3)))
        derivative = Const(0)
        Test().assert_dx_equal(derivative, to_dif)

    def test_param_log_param(self):
        to_dif = Log(Log(Const(E), X()), X())
        derivative = Divide(
            Subtract(Log(E, Log(E, X())), Const(1)),
            Multiply(X(), Power(Log(E, Log(E, X())), Const(2))))
        Test().assert_dx_equal(derivative, to_dif)


class TestPower(unittest.TestCase):
    def test_const_const(self):
        to_dif = Power(Const(5), Const(2))
        derivative = Const(0)
        Test().assert_dx_equal(derivative, to_dif)

    def test_const_const_rational_exp(self):
        to_dif = Power(Const(5), Const(1 / 2))
        derivative = Const(0)
        Test().assert_dx_equal(derivative, to_dif)

    def test_param_const(self):
        to_dif = Power(X(), Const(7))
        derivative = Multiply(Const(7), Power(X(), Const(6)))
        Test().assert_dx_equal(derivative, to_dif)

    def test_param_const_negative(self):
        to_dif = Power(X(), Const(-3))
        derivative = Multiply(Const(-3), Power(X(), Const(-4)))
        Test().assert_dx_equal(derivative, to_dif)

    def test_const_param(self):
        to_dif = Power(Const(4), X())
        derivative = Multiply(Power(Const(4), X()), Log(E, Const(4)))
        Test().assert_dx_equal(derivative, to_dif)

    def test_param_const_expression(self):
        to_dif = Power(X(), Power(Const(2), Const(2)))
        derivative = Multiply(Const(4), Power(X(), Const(3)))
        Test().assert_dx_equal(derivative, to_dif)

    def test_param_expression_const(self):
        to_dif = Power(Append(Const(2), Const(3)), X())
        derivative = Multiply(Power(Const(5), X()), Log(E, Const(5)))
        Test().assert_dx_equal(derivative, to_dif)

    def test_param_param_const(self):
        to_dif = Subtract(Append(Power(X(), Const(6)), Power(Const(2), Multiply(X(), Const(7)))),
                          Power(Const(3), Divide(Const(2), Const(5))))
        derivative = Append(Multiply(Const(6), Power(X(), Const(5))),
                            Multiply(Const(7), Multiply(Log(E, Const(2)), Power(Const(128), X()))))
        Test().assert_dx_equal(derivative, to_dif)

    def test_param_const_rational_exp(self):
        to_dif = Power(X(), Const(1 / 2))
        derivative = Divide(Const(1), Multiply(Const(2), Power(X(), Const(1 / 2))))
        Test().assert_dx_equal(derivative, to_dif)


def replace_all(expressions, to_replace, replacer):
    return [expr.replace(to_replace, replacer) for expr in expressions]


class TestSimpleParsing(unittest.TestCase):
    def assert_parsed_equals_expr(self, expr):
        parsed = parse(expr)
        self.assertEqual(simplify(expr), simplify(str(parsed)))

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

    def test_trigonometric(self):
        sin_x = 'sin(x)'
        cos_x = 'cos(x)'
        tan_x = 'tan(x)'
        cot_x = 'cot(x)'
        self.assert_parsed_equals_expr(sin_x)
        self.assert_parsed_equals_expr(cos_x)
        self.assert_parsed_equals_expr(tan_x)
        self.assert_parsed_equals_expr(cot_x)

    def test_logs(self):
        log2x = 'log(2,x)'
        lgx = 'log(10,x)'
        lnx = 'log(e,x)'
        self.assert_parsed_equals_expr(log2x)
        self.assert_parsed_equals_expr(lgx)
        self.assertEqual(sympify('1/log(x)'), simplify(str(parse(lnx))))


class TestComplexParsing(unittest.TestCase):
    def test_many(self):
        expressions = ['sin(x+3)',
                       'sin(pi-E)',
                       'sin(pi*E)',
                       '2*sin(x)',
                       'sin(sin(x))',
                       'sin(x+10/5)',
                       'sin(x*6)^2',
                       '1+sin(2*x)-x',
                       'sin(5)*sin(x)',
                       'sin(5)^sin(x)',
                       'sin(x)/(2*x^4)',
                       'sin(E^pi)^(x/5)']
        for expr in expressions:
            parsed = parse(expr)
            self.assertEqual(sympify(expr), simplify(str(parsed)))


class TestNoMultiSignAndBrackets(unittest.TestCase):
    def test_many(self):
        expressions = {'2x': '2*x',
                       '2(x+3)': '2*(x+3)',
                       '2sin(x)+x': '2*sin(x)+x',
                       'xx': 'x*x',
                       'x(2+x)': 'x*(2+x)',
                       'x3': 'x*3',
                       'xsin(x)': 'x*sin(x)',
                       '(x+1)(2^x+1)': '(x+1)*(2^x+1)',
                       '(x+1)x+1': '(x+1)*x+1',
                       '(x+1)sin(x)': '(x+1)*sin(x)',
                       'sinx': 'sin(x)',
                       'sinx+x': 'sin(x)+x',
                       'sin2x+x': 'sin(2*x)+x',
                       'sinx^3': 'sin(x^3)',
                       'sinxsinx': 'sin(x)*sin(x)',
                       'sin2xsin(x+1)': 'sin(2*x)*sin(x+1)',
                       'sin2xsin(x+1)*2+1': 'sin(2*x)*sin(x+1)*2+1',
                       'sin2x+sin(xsin(x+1))': 'sin(2*x)+sin(x*sin(x+1))',
                       'sin2x+sin(xsinx)+1': 'sin(2*x)+sin(x*sin(x))+1',
                       'ln((x^2+4)/(x-1))': 'log(E)/log((x^2+4)/(x-1))',
                       'lg(xsin(x^2)/x^2)': 'log(10)/log(x*sin(x^2)/x^2)',
                       'log(5, sin(x))': 'log(5)/log(sin(x))'}
        for expr, sympy_expr in expressions.items():
            parsed = parse(expr)
            self.assertEqual(sympify(sympy_expr), simplify(str(parsed)))


if __name__ == '__main__':
    unittest.main()
