from enum import Enum


class FuncType(Enum):
    constant = 1
    param = 2
    binary = 3
    # function = 4


class BinaryType(Enum):
    add = 1
    subtract = 2
    multiply = 3
    divide = 4


class OperandType(Enum):
    constant = 1
    param = 2


class Func:
    def __init__(self, func_type, operands, binary_type=None, function_type=None):
        self.type = func_type
        self.binary_type = binary_type
        self.function_type = function_type
        self.operands = operands

    def __eq__(self, other):
        return self.type == other.type and\
               self.binary_type == other.binary_type and\
               self.function_type == other.function_type and\
               self.operands == other.operands  # вопрос о коммутативности


class Differentiation:
    def differentiate(self, func: Func):
        if func.type == FuncType.constant:
            return Func(FuncType.constant, operands=[(OperandType.constant, 0)])  # [(type, value),...]
        elif func.type == FuncType.param:
            return Func(FuncType.constant, operands=[(OperandType.constant, 1)])
        else:
            if func.binary_type == BinaryType.add:
                return self.differentiate_sum(func)
            else:
                return self.differentiate_subtraction(func)
            # elif func.binary_type == BinaryType.multiply:
            #     return self.differentiate()
            # return self.differentiate_dividing(func)

    def differentiate_sum(self, func):
        left_operand = self.differentiate(func.operands[0][1])  # operands[i] - tuple
        right_operand = self.differentiate(func.operands[1][1])
        derivative = Func(FuncType.binary, binary_type=BinaryType.add,
                          operands=[left_operand, right_operand])
        return derivative

    def differentiate_subtraction(self, func):
        left_operand = self.differentiate(func.operands[0][1])
        right_operand = self.differentiate(func.operands[1][1])
        derivative = Func(FuncType.binary, binary_type=BinaryType.subtract,
                          operands=[left_operand, right_operand])
        return derivative

    def differentiate_multiplication(self, func):
        left_operand_derivative = self.differentiate(func.operands[0][1])
        right_operand_derivative = self.differentiate(func.operands[1][1])
        left_operand = Func(FuncType.binary, binary_type=BinaryType.multiply,
                            operands=[left_operand_derivative, func.operands[1][1]])
        right_operand = Func(FuncType.binary, binary_type=BinaryType.multiply,
                             operands=[right_operand_derivative, func.operands[0][1]])
        derivative = Func(FuncType.binary, binary_type=BinaryType.add,
                          operands=[left_operand, right_operand])
        return derivative

    # def differentiate_dividing(self, func):
    #     left_operand_derivative = self.differentiate(func.operands[0])
    #     right_operand_derivative = self.differentiate(func.operands[1])
    #     derivative = Func(FuncType.binary, binary_type=BinaryType.divide,
    #                       operands=[left_operand, right_operand])
