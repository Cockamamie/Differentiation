import unittest
from differentiation import *
from sympy import *
import numpy as np

values = [i * 0.1 for i in range(0, 50)]


class Test(unittest.TestCase):
    def assert_dx_equal(self, func, to_dif: Dx):
        x = Symbol('x')
        eps = 1e-7
        d = to_dif.dx()
        print(f'expr before simplify = {str(d)}')
        expr = simplify(str(d))
        print(f'expr after simplify = {expr}')
        for value in values:
            try:
                expected = (func(value + eps) - func(value)) / eps
                actual = expr.evalf(subs={x: value})
                self.assertAlmostEqual(expected, actual, delta=1e-3)
            except ZeroDivisionError:
                print('ZeroDivisionWarning')


class TestConstAndParam(unittest.TestCase):
    def test_const(self):
        def func(x):
            return 5
        to_dif = Const(5)
        Test().assert_dx_equal(func, to_dif)

    def test_param(self):
        def func(x):
            return x
        to_dif = X()
        Test().assert_dx_equal(func, to_dif)


class TestAddition(unittest.TestCase):
    def test_const_const(self):
        def func(x):
            return 5 + 1
        to_dif = Plus(Const(5), Const(1))
        Test().assert_dx_equal(func, to_dif)

    def test_const_param(self):
        def func(x):
            return 2 + x
        to_dif = Plus(Const(2), X())
        Test().assert_dx_equal(func, to_dif)

    def test_param_param(self):
        def func(x):
            return x + x
        to_dif = Plus(X(), X())
        Test().assert_dx_equal(func, to_dif)


class TestSubtraction(unittest.TestCase):
    def test_const_const(self):
        def func(x):
            return 5 - 1
        to_dif = Subtract(Const(5), Const(1))
        Test().assert_dx_equal(func, to_dif)

    def test_const_param(self):
        def func(x):
            return 2 - x
        to_dif = Subtract(Const(2), X())
        Test().assert_dx_equal(func, to_dif)

    def test_param_param(self):
        def func(x):
            return x - x
        to_dif = Subtract(X(), X())
        Test().assert_dx_equal(func, to_dif)


class TestMultiplication(unittest.TestCase):
    def test_const_const(self):
        def func(x):
            return 5 * 2
        to_dif = Multiply(Const(5), Const(2))
        Test().assert_dx_equal(func, to_dif)

    def test_const_param(self):
        def func(x):
            return 5 * x
        to_dif = Multiply(Const(5), X())
        Test().assert_dx_equal(func, to_dif)

    def test_param_param(self):
        def func(x):
            return x * x
        to_dif = Multiply(X(), X())
        Test().assert_dx_equal(func, to_dif)


class TestDivision(unittest.TestCase):
    def test_const_const(self):
        def func(x):
            return 5 / 2
        to_dif = Divide(Const(5), Const(2))
        Test().assert_dx_equal(func, to_dif)

    def test_const_param(self):
        def func(x):
            return 5 / x
        to_dif = Divide(Const(5), X())
        Test().assert_dx_equal(func, to_dif)

    def test_param_param(self):
        def func(x):
            return x / x
        to_dif = Divide(X(), X())
        Test().assert_dx_equal(func, to_dif)


class TestTrigonometry(unittest.TestCase):
    def test_sin_const(self):
        def func(x):
            return sin(5)
        to_dif = Sin(Const(5))
        Test().assert_dx_equal(func, to_dif)

    def test_sin_param(self):
        def func(x):
            return sin(x)
        to_dif = Sin(X())
        Test().assert_dx_equal(func, to_dif)

    def test_cos_const(self):
        def func(x):
            return cos(5)
        to_dif = Cos(Const(5))
        Test().assert_dx_equal(func, to_dif)

    def test_cos_param(self):
        def func(x):
            return cos(x)
        to_dif = Cos(X())
        Test().assert_dx_equal(func, to_dif)


if __name__ == '__main__':
    unittest.main()
