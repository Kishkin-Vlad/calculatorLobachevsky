# Сторонние библиотеки
# Импортируем очередь
from collections import deque as _deque


# Наши модули
from .Error import PolynomError


class _Monom(object):
    """
    Класс моном
    """

    def __init__(self, coefficient=0, variables=None):
        """
        :param coefficient: коэффициент монома
        :param variables: словарь с:
        ключи - название перемернных
        значениями - степенями переменных
        """

        if not isinstance(coefficient, (int, float, complex)):
            raise PolynomError('coefficient is not a number',
                               {'def': '__init__(for _Monom)', 'type': type(coefficient)})
        self.coefficient = coefficient

        if not (isinstance(variables, dict) or variables is None):
            raise PolynomError('variables is not a dict',
                               {'def': '__init__(for _Monom)', 'type': type(variables)})
        self.variables = {}
        if variables is not None:
            keys = variables.keys()
            for key in keys:
                if not isinstance(variables[key], (int, float, complex)):
                    raise PolynomError('variable is not a number',
                                       {'def': '__init__(for _Monom)', 'type': type(variables[key])})
                self.variables[key] = variables[key]

    def get_coefficient(self):
        """
        Получение коэффициента монома
        :return: коэффициент монома
        """

        return self.coefficient

    def get_power(self, variables):
        """
        Получение степени переменной
        :param variables: строка с названием переменной (или список строк)
        :return: степень переменной
        """

        if not isinstance(variables, (str, list)):
            raise PolynomError('variables is not a str or a list',
                               {'def': 'get_power(for _Monom)', 'type': type(variables)})

        if isinstance(variables, str):
            try:
                return self.variables[variables]
            except KeyError:
                raise PolynomError('no such variable',
                                   {'def': 'get_power(for _Monom)', 'variable': variables})

        if isinstance(variables, list):
            result = []
            for variable in variables:
                try:
                    result.append(self.variables[variable])
                except KeyError:
                    raise PolynomError('no such variable',
                                       {'def': 'get_power(for _Monom)', 'variable': variable})
            return result

    def get_variables(self):
        """
        Получение всех переменных с их степенями
        :return: словарь с:
        ключами - названиями переменных
        значениями - степенями переменных
        """

        return self.variables

    def __eq__(self, other):
        """
        Проверка на равенство - self == other
        :param other: моном или число
        :return: True - равны, False - не равны
        """

        if isinstance(other, _Monom):
            # Если равны коэф и переменные
            return self.get_coefficient() == other.get_coefficient() and self.get_variables() == other.get_variables()
        elif isinstance(other, (int, float, complex)):
            # Если нет переменных в мономе и коэф. монома равен числу
            return not self.get_variables() and self.get_coefficient() == other
        else:
            raise PolynomError('comparing a number with an incompatible type',
                               {'def': '__eq__(for _Monom)', 'type': type(other)})

    def __ne__(self, other):
        """
        Проверка на неравенство - self != other
        :param other: моном или число
        :return: True - не равны, False - равны
        """

        if isinstance(other, _Monom):
            # Если равны коэф и переменные
            return self.get_coefficient() != other.get_coefficient() or self.get_variables() != other.get_variables()
        elif isinstance(other, (int, float, complex)):
            # Если нет переменных в мономе и коэф. монома равен числу
            return self.get_variables() or self.get_coefficient() != other
        else:
            raise PolynomError('comparing a number with an incompatible type',
                               {'def': '__ne__(for _Monom)', 'type': type(other)})

    def __lt__(self, other):
        """
        Сравнение - self < other
        :param other: моном или число
        :return: True => self < other, False => self > other
        """

        if isinstance(other, _Monom):
            var1 = self.get_variables()
            var2 = other.get_variables()

            keys1 = sorted(var1)
            keys2 = sorted(var2)
            len1 = len(keys1)
            len2 = len(keys2)
            for i, (key1, key2) in enumerate(zip(keys1, keys2)):
                if key1 == key2:
                    if (i == len1 - 1 or i == len2 - 1) and len1 == len2:
                        if var1[key1] < var2[key2]:
                            return True
                        return False
                    else:
                        if var1[key1] > var2[key2]:
                            return False
                elif key1 > key2:
                    return False

            if len1 < len2:
                return True
            elif len1 > len2:
                return False
            if self.get_coefficient() >= other.get_coefficient():
                return False

            return True
        elif isinstance(other, (int, float, complex)):
            # Если нет переменных в мономе и коэф. монома равен числу
            return not self.get_variables() and self.get_coefficient() < other
        else:
            raise PolynomError('comparing a number with an incompatible type',
                               {'def': '__lt__(for _Monom)', 'type': type(other)})

    def __le__(self, other):
        """
        Сравнение - self <= other
        :param other: моном или число
        :return: True => self <= other, False => self >= other
        """

        if isinstance(other, _Monom):
            var1 = self.get_variables()
            var2 = other.get_variables()

            keys1 = sorted(var1)
            keys2 = sorted(var2)
            len1 = len(keys1)
            len2 = len(keys2)
            for i, (key1, key2) in enumerate(zip(keys1, keys2)):
                if key1 == key2:
                    if (i == len1 - 1 or i == len2 - 1) and len1 == len2:
                        if var1[key1] <= var2[key2]:
                            return True
                        return False
                    else:
                        if var1[key1] > var2[key2]:
                            return False
                elif key1 > key2:
                    return False

            if len1 < len2:
                return True
            elif len1 > len2:
                return False
            if self.get_coefficient() > other.get_coefficient():
                return False

            return True
        elif isinstance(other, (int, float, complex)):
            # Если нет переменных в мономе и коэф. монома равен числу
            return not self.get_variables() and self.get_coefficient() <= other
        else:
            raise PolynomError('comparing a number with an incompatible type',
                               {'def': '__lt__(for _Monom)', 'type': type(other)})

    def __gt__(self, other):
        """
        Сравнение - self > other
        :param other: моном или число
        :return: True => self > other, False => self > other
        """

        pass

    def __ge__(self, other):
        pass


class Polynom(object):

    def __init__(self):
        pass
