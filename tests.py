import unittest
from differentiation import *
from sympy import *

if __name__ == '__main__':
    unittest.main()

values = [i * 0.1 for i in range(0, 50)]


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

    def test_param_param_expression(self):
        func = Subtract(Multiply(Power(Const(2), X()), Multiply(Log(E, Const(2)), Cos(Power(Const(2), X())))),
                        Divide(Const(2), X()))
        to_dif = Subtract(Sin(Power(Const(2), X())), Log(Const(E), Power(X(), Const(2))))
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

    def test_param_param_expression(self):
        func = Append(Multiply(Multiply(Const(3), Power(Const(8), X())), Multiply(Log(E, Const(2)), Log(E, X()))),
                      Divide(Power(Const(8), X()), X()))
        to_dif = Multiply(Power(Const(2), Multiply(Const(3), X())), Log(Const(E), X()))
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

    def test_param_param_expression(self):
        func = Divide(Subtract(Multiply(Cos(Append(X(), Const(3))), X()), Sin(Append(X(), Const(3)))), Power(X(), Const(2)))
        to_dif = Divide(Sin(Append(X(), Const(3))), X())
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

    def test_sin_param_expression(self):
        func = Multiply(Multiply(Const(2), X()), Cos(Append(Power(X(), Const(2)), Sin(Const(9)))))
        to_dif = Sin(Append(Power(X(),Const(2)), Sin(Const(9))))
        Test().assert_dx_equal(func, to_dif)

    def test_cos_const(self):
        func = Const(0)
        to_dif = Cos(Const(5))
        Test().assert_dx_equal(func, to_dif)

    def test_cos_param(self):
        func = Multiply(Const(-1), Sin(X()))
        to_dif = Cos(X())
        Test().assert_dx_equal(func, to_dif)

    def test_cos_param_expression(self):
        func = negate(Divide(Multiply(Const(7), Sin(Divide(Multiply(Const(14), X()), Cos(Const(4))))), Cos(Const(4))))
        to_dif = Power(Cos(Divide(Multiply(Const(7), X()), Cos(Const(4)))), Const(2))
        Test().assert_dx_equal(func, to_dif)

    def test_tan_const(self):
        func = Const(0)
        to_dif = Tan(Const(5))
        Test().assert_dx_equal(func, to_dif)

    def test_tan_param(self):
        func = Divide(Const(1), Power(Cos(X()), Const(2)))
        to_dif = Tan(X())
        Test().assert_dx_equal(func, to_dif)

    def test_tan_param_expression(self):
        func = Multiply(Power(Const(6), X()),
                        Multiply(Log(Const(E), Const(6)), Power(Divide(Const(1), Cos(Power(Const(6), X()))), Const(2))))
        to_dif = Tan(Power(Multiply(Const(2), Const(3)), X()))
        Test().assert_dx_equal(func, to_dif)

    def test_cot_const(self):
        func = Const(0)
        to_dif = Cot(Const(5))
        Test().assert_dx_equal(func, to_dif)

    def test_cot_param(self):
        func = Divide(Const(-1), Power(Sin(X()), Const(2)))
        to_dif = Cot(X())
        Test().assert_dx_equal(func, to_dif)

    def test_cot_param_expression(self):
        func = Multiply(Multiply(X(), Power(Sin(Cot(Power(X(), Const(2)))), Const(-2))),
                        Multiply(Const(2), Power(Sin(Power(X(), Const(2))), Const(-2))))
        to_dif = Cot(Cot(Power(X(), Const(2))))
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

    def test_param_expression_param_expression(self):
        func = Const(0)
        to_dif = Log(Power(X(), Const(2)), Power(X(), Const(3)))
        Test().assert_dx_equal(func, to_dif)

    def test_param_log_param(self):
        func = Divide(Subtract(Log(E, Log(E, X())), Const(1)), Multiply(X(), Power(Log(E, Log(E, X())), Const(2))))
        to_dif = Log(Log(Const(E), X()), X())
        Test().assert_dx_equal(func, to_dif)


class TestPower(unittest.TestCase):
    def test_const_const(self):
        func = Const(0)
        to_dif = Power(Const(5), Const(2))
        Test().assert_dx_equal(func, to_dif)

    def test_const_const_rational_exp(self):
        func = Const(0)
        to_dif = Power(Const(5), Const(1/2))
        Test().assert_dx_equal(func, to_dif)

    def test_param_const(self):
        func = Multiply(Const(7), Power(X(), Const(6)))
        to_dif = Power(X(), Const(7))
        Test().assert_dx_equal(func, to_dif)

    def test_param_const_negative(self):
        func = Multiply(Const(-3), Power(X(), Const(-4)))
        to_dif = Power(X(), Const(-3))
        Test().assert_dx_equal(func, to_dif)

    def test_const_param(self):
        func = Multiply(Power(Const(4), X()), Log(E, Const(4)))
        to_dif = Power(Const(4), X())
        Test().assert_dx_equal(func, to_dif)

    def test_param_const_expression(self):
        func = Multiply(Const(4), Power(X(), Const(3)))
        to_dif = Power(X(), Power(Const(2), Const(2)))
        Test().assert_dx_equal(func, to_dif)

    def test_param_expression_const(self):
        func = Multiply(Power(Const(5), X()), Log(E, Const(5)))
        to_dif = Power(Append(Const(2), Const(3)), X())
        Test().assert_dx_equal(func, to_dif)

    def test_param_param_const(self):
        func = Append(Multiply(Const(6), Power(X(), Const(5))),
                      Multiply(Const(7), Multiply(Log(E, Const(2)), Power(Const(128), X()))))
        to_dif = Subtract(Append(Power(X(), Const(6)), Power(Const(2), Multiply(X(), Const(7)))),
                          Power(Const(3), Divide(Const(2), Const(5))))
        print(to_dif)
        print(simplify(str(to_dif)))
        Test().assert_dx_equal(func, to_dif)


