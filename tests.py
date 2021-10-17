import math
import unittest
from differentiation import FuncType, BinaryType, OperandType, Func, Differentiation
#import numpy as np


# def assert_derivatives_equal(func):
#     eps = 1e-7
#     df = Differentiation().differentiate(func)
#     for x in list(np.arange(0, 5, 0.1)):
#         expected = (func(x + eps) - func(x)) / eps
#         actual = df(x)
#         assert abs(expected - actual) < 1e-5, f'{func.__name__}'


class TestSimpleDifferentiation(unittest.TestCase):
    def test_constant(self):
        func = Func(FuncType.constant, operands=[(OperandType.constant, 5)])
        actual = Differentiation().differentiate(func)
        expected = Func(FuncType.constant, operands=[(OperandType.constant, 0)])
        self.assertEqual(expected, actual)

    def test_parameter(self):
        func = Func(FuncType.param, operands=[(OperandType.param, 1)])
        actual = Differentiation().differentiate(func)
        expected = Func(FuncType.constant, operands=[(OperandType.constant, 1)])
        self.assertEqual(expected, actual)

    def test_parameter_int_power(self):
        def param_int_power(x): return x**5
        self.assertEqual(expected, actual)

    def test_parameter_rational_power(self):
        def param_rational_power(x): return x**(3 / 7)
        self.assertEqual(expected, actual)

    def test_constant_power(self):
        def const_power(x): return 6**7
        self.assertEqual(expected, actual)


class TestFuncsDifferentiation(unittest.TestCase):
    def test_log(self):
        def log_2(x): return math.log(x, 2)
        def log_e(x): return math.log(x, math.exp(1))
        def log_5(x): return math.log(x, 5)
        def log_10(x): return math.log(x, 5)
        logs = [log_2, log_e, log_5, log_10]
        for log in logs:
            self.assertEqual(expected, actual)

    def test_sin(self):
        def sin(x): return math.sin(x)
        self.assertEqual(expected, actual)

    def test_cos(self):
        def cos(x): return math.cos(x)
        self.assertEqual(expected, actual)

    def test_tan(self):
        def tg(x): return math.tan(x)
        self.assertEqual(expected, actual)

    def test_cot(self):
        def ctg(x): return 1 / math.tan(x)
        self.assertEqual(expected, actual)

    def test_arc_sin(self):
        def asin(x): return math.asin(x)
        self.assertEqual(expected, actual)

    def test_arc_cos(self):
        def acos(x): return math.acos(x)
        self.assertEqual(expected, actual)

    def test_arc_tan(self):
        def atan(x): return math.atan(x)
        self.assertEqual(expected, actual)

    def test_arc_cot(self):
        def acot(x): return math.pi / 2 - math.atan(x)
        self.assertEqual(expected, actual)


class TestSimpleBinaryOperationsDifferentiation(unittest.TestCase):
    def test_adding_consts(self):
        func = Func(FuncType.binary, binary_type=BinaryType.add,
                    operands=[(OperandType.constant, 4), (OperandType.constant, 7)])
        actual = Differentiation().differentiate(func)
        expected = Func(FuncType.binary, binary_type=BinaryType.add,
                        operands=[(OperandType.constant, 0), (OperandType.constant, 0)])
        # TODO: 0+0 = 0 (упростить, если возможно)
        self.assertEqual(expected, actual)

    def test_multiplying(self):
        pass

    def test_subtracting(self):
        func = Func(FuncType.binary, binary_type=BinaryType.subtract,
                    operands=[(OperandType.constant, 4), (OperandType.constant, 7)])
        actual = Differentiation.differentiate(func)
        expected = Func(FuncType.binary, binary_type=BinaryType.subtract,
                        operands=[(OperandType.constant, 0), (OperandType.constant, 0)])

    def test_dividing(self):
        pass


class TestParsing(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
