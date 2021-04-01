# Сторонние библиотеки
# Испортируем очередь
from collections import deque


class _Lexem(object):

    def __init__(self, expression, typeElement, value=-1, priority=-1):
        self.str = expression
        self.typeElement = typeElement
        self.value = value
        self.priority = priority

    def __eq__(self, other):
        pass
    
    def __str__(self):
        return self.str


class Expression(object):

    def __init__(self):
        pass

    def getInputExpression(self):
        pass

    def getOutputExpression(self):
        pass

    def addVal(self):
        pass

    def convertToRevPolNot(self):
        pass

    def calculateExpression(self):
        pass

