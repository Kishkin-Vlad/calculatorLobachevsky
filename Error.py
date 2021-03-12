"""

"""


class Error(Exception):

    def __init__(self, text):
        self.text = text


class MatrixError(Error):

    def __init__(self, text: str, arguments: dict):
        self.text = text
        self.arguments = arguments

    def __str__(self):
        result = '{} ('.format(self.text)
        for key, value in self.arguments.items():
            result = '{}{}={}, '.format(result, key, value)
        result = '{})'.format(result[:-2])

        return result
