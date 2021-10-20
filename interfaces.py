from abc import ABCMeta, abstractmethod


class Dx:
    __metaclass__ = ABCMeta

    @abstractmethod
    def dx(self): raise NotImplementedError

    @abstractmethod
    def __str__(self): raise NotImplementedError


class Binary:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, left: Dx, right: Dx): raise NotImplementedError


class Unary:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, arg: Dx): raise NotImplementedError
