# Сторонние библиотеки
from copy import deepcopy
# Импортируем очередь
from collections import deque as _deque


# Наши модули
from .Error import PolynomError
from .fraction import Fraction


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

        if not isinstance(coefficient, (int, float, complex, Fraction)):
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
                if not isinstance(variables[key], (int, float, complex, Fraction)):
                    raise PolynomError('variable is not a number',
                                       {'def': '__init__(for _Monom)', 'type': type(variables[key])})
                self.variables[key] = variables[key]

    def get_coefficient(self):
        """
        Получение коэффициента монома
        :return: коэффициент монома
        """

        return self.coefficient

    def get_power(self, variables) -> list or str:
        """
        Получение степени переменной
        :param variables: строка с названием переменной (или список строк)
        :return: степень переменной/ных
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

    def get_variables(self) -> dict:
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
        elif isinstance(other, (int, float, complex, Fraction)):
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
        elif isinstance(other, (int, float, complex, Fraction)):
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
            for i, (key1, key2) in enumerate(zip(keys1, keys2)):
                if key1 == key2:
                    if var1[key1] < var2[key2]:
                        return True
                    elif var1[key1] > var2[key2]:
                        return False
                elif key1 > key2:
                    return True
                elif key1 < key2:
                    return False
            len1 = len(keys1)
            len2 = len(keys2)
            if len1 < len2:
                return True
            elif len1 > len2:
                return False

            if self.get_coefficient() >= other.get_coefficient():
                return False
            return True

        elif isinstance(other, (int, float, complex, Fraction)):
            # Если нет переменных в мономе и коэф. монома равен числу
            if not self.get_variables() and self.get_coefficient() < other:
                return True
            return False
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
        elif isinstance(other, (int, float, complex, Fraction)):
            # Если нет переменных в мономе и коэф. монома равен числу
            if not self.get_variables() and self.get_coefficient() <= other:
                return True
            return False
        else:
            raise PolynomError('comparing a number with an incompatible type',
                               {'def': '__le__(for _Monom)', 'type': type(other)})

    def __gt__(self, other):
        """
        Сравнение - self > other
        :param other: моном или число
        :return: True => self > other, False => self < other
        """

        if isinstance(other, _Monom):

            var1 = self.get_variables()
            var2 = other.get_variables()

            keys1 = sorted(var1)
            keys2 = sorted(var2)
            for i, (key1, key2) in enumerate(zip(keys1, keys2)):
                if key1 == key2:
                    if var1[key1] > var2[key2]:
                        return True
                    elif var1[key1] < var2[key2]:
                        return False
                elif key1 < key2:
                    return True
                elif key1 > key2:
                    return False
            len1 = len(keys1)
            len2 = len(keys2)
            if len1 > len2:
                return True
            elif len1 < len2:
                return False

            if self.get_coefficient() <= other.get_coefficient():
                return False
            return True

        elif isinstance(other, (int, float, complex, Fraction)):
            # Если нет переменных в мономе и коэф. монома равен числу
            if self.get_variables() or self.get_coefficient() > other:
                return True
            return False
        else:
            raise PolynomError('comparing a number with an incompatible type',
                               {'def': '__lt__(for _Monom)', 'type': type(other)})

    def __ge__(self, other):
        """
        Сравнение - self >= other
        :param other: моном или число
        :return: True => self >= other, False => self <= other
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
                        if var1[key1] > var2[key2]:
                            return True
                        elif var1[key1] < var2[key2]:
                            return False
                    else:
                        if var1[key1] < var2[key2]:
                            return False
                elif key1 < key2:
                    return False

            if len1 > len2:
                return True
            elif len1 < len2:
                return False
            if self.get_coefficient() < other.get_coefficient():
                return False

            return True
        elif isinstance(other, (int, float, complex, Fraction)):
            # Если нет переменных в мономе и коэф. монома равен числу
            if self.get_variables() or self.get_coefficient() >= other:
                return True
            return False
        else:
            raise PolynomError('comparing a number with an incompatible type',
                               {'def': '__le__(for _Monom)', 'type': type(other)})

    def __neg__(self):
        """
        Унарный минус
        """

        tmp = deepcopy(self)
        tmp.coefficient = -tmp.coefficient

        return tmp

    def __add__(self, other):
        """
        Сложение монома и монома (= self + other)
        """

        if isinstance(other, _Monom):
            if self.get_variables() != other.get_variables():
                raise PolynomError('monomials of different degrees', {'def': '__add__(for _Monom)',
                                   'vars1': self.get_variables(), 'vars2': other.get_variables()})
            tmp = deepcopy(self)
            tmp.coefficient += other.coefficient

            return tmp
        else:
            raise PolynomError('addition of a monomial not to a monomial',
                               {'def': '__add__(for _Monom)', 'type': type(other)})

    def __iadd__(self, other):
        """
        Сложение монома и монома (self += other)
        """

        if isinstance(other, _Monom):
            if self.get_variables() != other.get_variables():
                raise PolynomError('monomials of different degrees', {'def': '__iadd__(for _Monom)',
                                                                      'vars1': self.get_variables(),
                                                                      'vars2': other.get_variables()})
            self.coefficient += other.coefficient

            return self
        else:
            raise PolynomError('addition of a monomial not to a monomial',
                               {'def': '__iadd__(for _Monom)', 'type': type(other)})

    def __sub__(self, other):
        """
        Вычитание монома и монома (= self - other)
        """

        if isinstance(other, _Monom):
            if self.get_variables() != other.get_variables():
                raise PolynomError('monomials of different degrees', {'def': '__sub__(for _Monom)',
                                                                      'vars1': self.get_variables(),
                                                                      'vars2': other.get_variables()})
            tmp = deepcopy(self)
            tmp.coefficient -= other.coefficient

            return tmp
        else:
            raise PolynomError('addition of a monomial not to a monomial',
                               {'def': '__sub__(for _Monom)', 'type': type(other)})

    def __isub__(self, other):
        """
        Вычитание монома и монома (self -= other)
        """

        if isinstance(other, _Monom):
            if self.get_variables() != other.get_variables():
                raise PolynomError('monomials of different degrees', {'def': '__isub__(for _Monom)',
                                                                      'vars1': self.get_variables(),
                                                                      'vars2': other.get_variables()})
            self.coefficient -= other.coefficient

            return self
        else:
            raise PolynomError('addition of a monomial not to a monomial',
                               {'def': '__isub__(for _Monom)', 'type': type(other)})

    def __mul__(self, other):
        """
        Умножение монома на число/моном (= self * other)
        """

        if isinstance(other, (int, float, complex, Fraction)):
            tmp = deepcopy(self)
            tmp.coefficient *= other
            return tmp
        elif isinstance(other, _Monom):
            tmp = deepcopy(self)
            tmp.coefficient *= other.coefficient

            variables1 = tmp.get_variables()
            variables2 = other.get_variables()
            keys = variables2.keys()
            for key in keys:
                if key in variables1:
                    tmp.variables[key] += variables2[key]
                else:
                    tmp.variables[key] = variables2[key]

            return tmp
        else:
            raise PolynomError('multiplication of a monomial not by a number/monomial',
                               {'def': '__mul__(for _Monom)', 'type': type(other)})

    def __rmul__(self, other):
        """
        Правое умножение монома на число/моном  (= other * self)
        """

        if isinstance(other, (int, float, complex, Fraction)):
            tmp = deepcopy(self)
            tmp.coefficient *= other
            return tmp
        elif isinstance(other, _Monom):
            tmp = deepcopy(self)
            tmp.coefficient *= other.coefficient

            variables1 = tmp.get_variables()
            variables2 = other.get_variables()
            keys = variables2.keys()
            for key in keys:
                if key in variables1:
                    tmp.variables[key] += variables2[key]
                else:
                    tmp.variables[key] = variables2[key]

            return tmp
        else:
            raise PolynomError('multiplication of a monomial not by a number/monomial',
                               {'def': '__rmul__(for _Monom)', 'type': type(other)})

    def __imul__(self, other):
        """
        Умножение монома на число/моном (self *= other)
        """

        if isinstance(other, (int, float, complex, Fraction)):
            self.coefficient *= other
            return self
        elif isinstance(other, _Monom):
            self.coefficient *= other.coefficient

            variables1 = self.get_variables()
            variables2 = other.get_variables()
            keys = variables2.keys()
            for key in keys:
                if key in variables1:
                    self.variables[key] += variables2[key]
                else:
                    self.variables[key] = variables2[key]

            return self
        else:
            raise PolynomError('multiplication of a monomial not by a number/monomial',
                               {'def': '__imul__(for _Monom)', 'type': type(other)})

    def __str__(self):
        result = '{}'.format(self.get_coefficient())

        variables = self.get_variables()
        if variables:
            keys = variables.keys()
            for var in keys:
                result += '*{}^'.format(var)
                result += '{}'.format(variables[var])

        return result

    def __repr__(self):
        result = '{}'.format(self.get_coefficient())

        variables = self.get_variables()
        if variables:
            keys = variables.keys()
            for var in keys:
                result += '*{}^'.format(var)
                result += '{}'.format(variables[var])

        return result


class Polynom(object):
    """
    Класс полином
    """

    def __init__(self, obj=None):
        """
        Инициализация
        """

        self.list_monom = []
        if obj is None:
            self.list_monom.append(_Monom())
        elif isinstance(obj, (int, float, complex, Fraction)):
            self.list_monom.append(_Monom(obj))
        elif isinstance(obj, _Monom):
            self.list_monom.append(deepcopy(obj))
        elif isinstance(obj, Polynom):
            self.list_monom = deepcopy(obj.list_monom)
        else:
            raise PolynomError('polynomial initialization not with number/monomial/polynomial',
                               {'def': '__init__(for _Polynom)', 'type': type(obj)})

    def __add__(self, other):
        """
        Сложение полинома с мономом/полиномом
        """

        if isinstance(other, _Monom):
            tmp = deepcopy(self)
            length = len(tmp.list_monom) - 1
            if other.get_coefficient() != 0:
                if tmp.list_monom[0].get_coefficient() != 0:
                    for i, mon1 in enumerate(tmp.list_monom):
                        if other.get_variables() == mon1.get_variables():
                            mon1 += deepcopy(other)

                            if mon1.get_coefficient() == 0:
                                tmp.list_monom.pop(i)
                                if not length:
                                    tmp.list_monom.append(_Monom(0))

                            break
                        elif other > mon1:
                            tmp.list_monom.insert(i, other)
                            break
                        elif other < mon1 and i == length:
                            tmp.list_monom.append(other)
                            break
                else:
                    tmp.list_monom[0] = deepcopy(other)
            return tmp
        elif isinstance(other, Polynom):
            tmp = deepcopy(self)
            if tmp.list_monom[0].get_coefficient() != 0:
                for mon2 in other.list_monom:
                    length = len(tmp.list_monom) - 1
                    if mon2.get_coefficient() != 0:
                        for i, mon1 in enumerate(tmp.list_monom):
                            if mon2.get_variables() == mon1.get_variables():
                                mon1 += mon2

                                if mon1.get_coefficient() == 0 and length:
                                    tmp.list_monom.pop(i)

                                break
                            elif mon2 > mon1:
                                tmp.list_monom.insert(i, mon2)
                                break
                            elif mon2 < mon1 and i == length:
                                tmp.list_monom.append(mon2)
                                break
            else:
                tmp = deepcopy(other)

            return tmp
        else:
            raise PolynomError('addition of a polynomial not with a number/monomial/polynomial',
                               {'def': '__add__(for _Polynom)', 'type': type(other)})

    def __radd__(self, other):
        """
        Правое сложение полинома с мономом/полиномом
        """

        if isinstance(other, _Monom):
            tmp = deepcopy(self)
            length = len(tmp.list_monom) - 1
            if other.get_coefficient() != 0:
                if tmp.list_monom[0].get_coefficient() != 0:
                    for i, mon1 in enumerate(tmp.list_monom):
                        if other.get_variables() == mon1.get_variables():
                            mon1 += deepcopy(other)

                            if mon1.get_coefficient() == 0:
                                tmp.list_monom.pop(i)
                                if not length:
                                    tmp.list_monom.append(_Monom(0))

                            break
                        elif other > mon1:
                            tmp.list_monom.insert(i, other)
                            break
                        elif other < mon1 and i == length:
                            tmp.list_monom.append(other)
                            break
                else:
                    tmp.list_monom[0] = deepcopy(other)
            return tmp
        elif isinstance(other, Polynom):
            tmp = deepcopy(self)
            if tmp.list_monom[0].get_coefficient() != 0:
                for mon2 in other.list_monom:
                    length = len(tmp.list_monom) - 1
                    if mon2.get_coefficient() != 0:
                        for i, mon1 in enumerate(tmp.list_monom):
                            if mon2.get_variables() == mon1.get_variables():
                                mon1 += mon2

                                if mon1.get_coefficient() == 0 and length:
                                    tmp.list_monom.pop(i)

                                break
                            elif mon2 > mon1:
                                tmp.list_monom.insert(i, mon2)
                                break
                            elif mon2 < mon1 and i == length:
                                tmp.list_monom.append(mon2)
                                break
            else:
                tmp = deepcopy(other)

            return tmp
        else:
            raise PolynomError('addition of a polynomial not with a number/monomial/polynomial',
                               {'def': '__radd__(for _Polynom)', 'type': type(other)})

    def __iadd__(self, other):
        """
        Cложение полинома с мономом/полиномом
        """

        if isinstance(other, _Monom):
            length = len(self.list_monom) - 1
            if other.get_coefficient() != 0:
                if self.list_monom[0].get_coefficient() != 0:
                    for i, mon1 in enumerate(self.list_monom):
                        if other.get_variables() == mon1.get_variables():
                            mon1 += deepcopy(other)

                            if mon1.get_coefficient() == 0:
                                self.list_monom.pop(i)
                                if not length:
                                    self.list_monom.append(_Monom(0))

                            break
                        elif other > mon1:
                            self.list_monom.insert(i, other)
                            break
                        elif other < mon1 and i == length:
                            self.list_monom.append(other)
                            break
                else:
                    self.list_monom[0] = deepcopy(other)
            return self
        elif isinstance(other, Polynom):
            if self.list_monom[0].get_coefficient() != 0:
                for mon2 in other.list_monom:
                    length = len(self.list_monom) - 1
                    if mon2.get_coefficient() != 0:
                        for i, mon1 in enumerate(self.list_monom):
                            if mon2.get_variables() == mon1.get_variables():
                                mon1 += mon2

                                if mon1.get_coefficient() == 0 and length:
                                    self.list_monom.pop(i)

                                break
                            elif mon2 > mon1:
                                self.list_monom.insert(i, mon2)
                                break
                            elif mon2 < mon1 and i == length:
                                self.list_monom.append(mon2)
                                break
            else:
                return deepcopy(other)

            return self
        else:
            raise PolynomError('addition of a polynomial not with a number/monomial/polynomial',
                               {'def': '__iadd__(for _Polynom)', 'type': type(other)})

    def __sub__(self, other):
        """
        Разность полинома с мономом/полиномом
        """

        if isinstance(other, _Monom):
            tmp = deepcopy(self)
            length = len(tmp.list_monom) - 1
            if other.get_coefficient() != 0:
                if tmp.list_monom[0].get_coefficient() != 0:
                    for i, mon1 in enumerate(tmp.list_monom):
                        if other.get_variables() == mon1.get_variables():
                            mon1 -= deepcopy(other)

                            if mon1.get_coefficient() == 0:
                                tmp.list_monom.pop(i)
                                if not length:
                                    tmp.list_monom.append(_Monom(0))

                            break
                        elif other > mon1:
                            tmp.list_monom.insert(i, -other)
                            break
                        elif other < mon1 and i == length:
                            tmp.list_monom.append(-other)
                            break
                else:
                    tmp.list_monom[0] = deepcopy(-other)

            return tmp
        elif isinstance(other, Polynom):
            tmp = deepcopy(self)
            if tmp.list_monom[0].get_coefficient() != 0:
                for mon2 in other.list_monom:
                    length = len(tmp.list_monom) - 1
                    if mon2.get_coefficient() != 0:
                        for i, mon1 in enumerate(tmp.list_monom):
                            if mon2.get_variables() == mon1.get_variables():
                                mon1 -= mon2

                                if mon1.get_coefficient() == 0 and length:
                                    tmp.list_monom.pop(i)

                                break
                            elif mon2 > mon1:
                                tmp.list_monom.insert(i, -mon2)
                                break
                            elif mon2 < mon1 and i == length:
                                tmp.list_monom.append(-mon2)
                                break
            else:
                tmp = deepcopy(-other)

            return tmp
        else:
            raise PolynomError('difference of a polynomial not with a number/monomial/polynomial',
                               {'def': '__sub__(for _Polynom)', 'type': type(other)})

    def __rsub__(self, other):
        """
        Правая разница полинома с мономом/полиномом
        """

        if isinstance(other, _Monom):
            tmp = deepcopy(self)
            length = len(tmp.list_monom) - 1
            if other.get_coefficient() != 0:
                if tmp.list_monom[0].get_coefficient() != 0:
                    for i, mon1 in enumerate(tmp.list_monom):
                        if other.get_variables() == mon1.get_variables():
                            mon1 -= deepcopy(other)

                            if mon1.get_coefficient() == 0:
                                tmp.list_monom.pop(i)
                                if not length:
                                    tmp.list_monom.append(_Monom(0))

                            break
                        elif other > mon1:
                            tmp.list_monom.insert(i, -other)
                            break
                        elif other < mon1 and i == length:
                            tmp.list_monom.append(-other)
                            break
                else:
                    tmp.list_monom[0] = deepcopy(-other)

            return tmp
        elif isinstance(other, Polynom):
            tmp = deepcopy(self)
            if tmp.list_monom[0].get_coefficient() != 0:
                for mon2 in other.list_monom:
                    length = len(tmp.list_monom) - 1
                    if mon2.get_coefficient() != 0:
                        for i, mon1 in enumerate(tmp.list_monom):
                            if mon2.get_variables() == mon1.get_variables():
                                mon1 -= mon2

                                if mon1.get_coefficient() == 0 and length:
                                    tmp.list_monom.pop(i)

                                break
                            elif mon2 > mon1:
                                tmp.list_monom.insert(i, -mon2)
                                break
                            elif mon2 < mon1 and i == length:
                                tmp.list_monom.append(-mon2)
                                break
            else:
                tmp = deepcopy(-other)

            return tmp
        else:
            raise PolynomError('difference of a polynomial not with a number/monomial/polynomial',
                               {'def': '__rsub__(for _Polynom)', 'type': type(other)})

    def __isub__(self, other):
        """
        Разница полинома с мономом/полиномом
        """

        if isinstance(other, _Monom):
            length = len(self.list_monom) - 1
            if other.get_coefficient() != 0:
                if self.list_monom[0].get_coefficient() != 0:
                    for i, mon1 in enumerate(self.list_monom):
                        if other.get_variables() == mon1.get_variables():
                            mon1 -= deepcopy(other)

                            if mon1.get_coefficient() == 0:
                                self.list_monom.pop(i)
                                if not length:
                                    self.list_monom.append(_Monom(0))

                            break
                        elif other > mon1:
                            self.list_monom.insert(i, -other)
                            break
                        elif other < mon1 and i == length:
                            self.list_monom.append(-other)
                            break
                else:
                    self.list_monom[0] = deepcopy(-other)

            return self
        elif isinstance(other, Polynom):
            if self.list_monom[0].get_coefficient() != 0:
                for mon2 in other.list_monom:
                    length = len(self.list_monom) - 1
                    if mon2.get_coefficient() != 0:
                        for i, mon1 in enumerate(self.list_monom):
                            if mon2.get_variables() == mon1.get_variables():
                                mon1 -= mon2

                                if mon1.get_coefficient() == 0 and length:
                                    self.list_monom.pop(i)

                                break
                            elif mon2 > mon1:
                                self.list_monom.insert(i, -mon2)
                                break
                            elif mon2 < mon1 and i == length:
                                self.list_monom.append(-mon2)
                                break
            else:
                return deepcopy(-other)

            return self
        else:
            raise PolynomError('difference of a polynomial not with a number/monomial/polynomial',
                               {'def': '__isub__(for _Polynom)', 'type': type(other)})

    def __mul__(self, other):
        """
        Умножение полиномов с числами/мономами/полиномами
        """

        if isinstance(other, (int, float, complex, Fraction)):
            if other != 0:
                tmp = deepcopy(self)
                for elem in tmp.list_monom:
                    elem *= deepcopy(other)

                return tmp
            else:
                return Polynom()
        elif isinstance(other, _Monom):
            if other.get_coefficient() != 0:
                tmp = deepcopy(self)
                for elem in tmp.list_monom:
                    elem *= deepcopy(other)

                return tmp
            else:
                return Polynom()
        elif isinstance(other, Polynom):
            tmp = deepcopy(self)
            for mon2 in other.list_monom:
                if mon2.get_coefficient() != 0:
                    for mon1 in tmp.list_monom:
                        if mon1.get_coefficient() != 0:
                            mon1 *= mon2

            return tmp
        else:
            raise PolynomError('multiplication of a polynomial not by a number/monomial/polynomial',
                               {'def': '__mul__(for _Polynom)', 'type': type(other)})

    def __rmul__(self, other):
        """
        Правое умножение полиномов с числами/мономами/полиномами
        """

        if isinstance(other, (int, float, complex, Fraction)):
            if other != 0:
                tmp = deepcopy(self)
                for elem in tmp.list_monom:
                    elem *= deepcopy(other)

                return tmp
            else:
                return Polynom()
        elif isinstance(other, _Monom):
            if other.get_coefficient() != 0:
                tmp = deepcopy(self)
                for elem in tmp.list_monom:
                    elem *= deepcopy(other)

                return tmp
            else:
                return Polynom()
        elif isinstance(other, Polynom):
            tmp = deepcopy(self)
            for mon2 in other.list_monom:
                if mon2.get_coefficient() != 0:
                    for mon1 in tmp.list_monom:
                        if mon1.get_coefficient() != 0:
                            mon1 *= mon2

            return tmp
        else:
            raise PolynomError('multiplication of a polynomial not by a number/monomial/polynomial',
                               {'def': '__rmul__(for _Polynom)', 'type': type(other)})

    def __imul__(self, other):
        """
        Умножение полиномов с числами/мономами/полиномами
        """

        if isinstance(other, (int, float, complex, Fraction)):
            if other != 0:
                for elem in self.list_monom:
                    elem *= deepcopy(other)

                return self
            else:
                return Polynom()
        elif isinstance(other, _Monom):
            if other.get_coefficient() != 0:
                for elem in self.list_monom:
                    elem *= deepcopy(other)

                return self
            else:
                return Polynom()
        elif isinstance(other, Polynom):
            for mon2 in other.list_monom:
                if mon2.get_coefficient() != 0:
                    for mon1 in self.list_monom:
                        if mon1.get_coefficient() != 0:
                            mon1 *= mon2

            return self
        else:
            raise PolynomError('multiplication of a polynomial not by a number/monomial/polynomial',
                               {'def': '__rmul__(for _Polynom)', 'type': type(other)})

    def __neg__(self):
        """
        Унарный минус
        """

        tmp = deepcopy(self)
        for mon in tmp.list_monom:
            mon = -mon

        return tmp

    def __str__(self):
        result = ''
        for i, mon in enumerate(self.list_monom):
            if i == 0:
                result += str(mon)
            else:
                if mon.get_coefficient() >= 0:
                    result += '+{}'.format(mon)
                else:
                    result += str(mon)

        return result

    def __repr__(self):
        result = ''
        for i, mon in enumerate(self.list_monom):
            if i == 0:
                result += str(mon)
            else:
                if mon.get_coefficient() >= 0:
                    result += '+{}'.format(mon)
                else:
                    result += str(mon)

        return result
