"""

"""


class Error(Exception):
    """
    Общие ошибки библиотеки calculatorLobachevsky
    """

    def __init__(self, text: str, arguments: dict):
        self.text = text
        self.arguments = arguments

    def __str__(self):
        result = '{} ('.format(self.text)
        for key, value in self.arguments.items():
            result = '{}{}={}, '.format(result, key, value)
        result = '{})'.format(result[:-2])

        return result


class ExpressionError(Error):
    """
    Ошибки связанные с работой с выражениями
    """

    def __init__(self, text: str, arguments: dict):
        self.text = text
        self.arguments = arguments

    def __str__(self):
        result = '{} ('.format(self.text)
        for key, value in self.arguments.items():
            result = '{}{}={}, '.format(result, key, value)
        result = '{})'.format(result[:-2])

        return result


class FractionError(Error):
    """
    Ошибки связанные с работой с дробью
    """

    def __init__(self, text: str, arguments: dict):
        self.text = text
        self.arguments = arguments

    def __str__(self):
        result = '{} ('.format(self.text)
        for key, value in self.arguments.items():
            result = '{}{}={}, '.format(result, key, value)
        result = '{})'.format(result[:-2])

        return result


class MatrixError(Error):
    """
    Ошибки связанные с работой с матрицами
    """

    def __init__(self, text: str, arguments: dict):
        self.text = text
        self.arguments = arguments

    def __str__(self):
        result = '{} ('.format(self.text)
        for key, value in self.arguments.items():
            result = '{}{}={}, '.format(result, key, value)
        result = '{})'.format(result[:-2])

        return result


class PolynomError(Error):
    """
    Ошибки связанные с работой с полиномами
    """

    def __init__(self, text: str, arguments: dict):
        self.text = text
        self.arguments = arguments

    def __str__(self):
        result = '{} ('.format(self.text)
        for key, value in self.arguments.items():
            result = '{}{}={}, '.format(result, key, value)
        result = '{})'.format(result[:-2])

        return result
