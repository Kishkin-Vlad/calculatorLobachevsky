# Сторонние библиотеки
from copy import deepcopy


# Наши модули
from .Error import FractionError


def _factor(number: int):
    """
    Получить из числа его простые множители
    :param number: целочисленное число
    :return: список множителей
    """
    """
    Проверяем делимость number на натуральные числа подряд, начиная с 2
    Если prime_number делитель number, то делим number на prime_number
    Продолжаем перебор до sqrt(number)
    Если в конце number != 1 => number так же является простым делителем
    """

    if not isinstance(number, int):
        raise FractionError('not integer number', {'def': 'factor (prime factorization)', 'type': type(number)})

    number = abs(number)
    numbers = []
    prime_number = 2
    while prime_number ** 2 <= number:
        if number % prime_number == 0:
            numbers.append(prime_number)
            number //= prime_number
        else:
            prime_number += 1
    if number > 1:
        numbers.append(number)

    return numbers


def _removing_identical_elements(list1: list, list2: list):
    """
    Удаляет одинаковые элементы из двух массивов
    Пример: [2, 2, 3] и [2, 2, 2, 5] => [3] и [2, 5]
    :param list1: Первый массив
    :param list2: Второй массив
    :return: Очищенные массивы
    """

    new_list1 = deepcopy(list1)
    new_list2 = deepcopy(list2)
    # Схема для динамических списков (из которых
    # удаляются элементы => меняется длина списка)
    i = 0
    j = 0
    next_b = True
    while i < len(new_list1):
        j = 0
        while j < len(new_list2):
            from_numerator = new_list1[i]
            from_denominator = new_list2[j]
            if from_numerator == from_denominator:
                new_list1.pop(i)
                new_list2.pop(j)
                next_b = False
                break
            else:
                j += 1
        if next_b:
            i += 1
        next_b = True

    return new_list1, new_list2


class Fraction(object):
    """
    Объект дробь, нужен для приведения матрицы к треугольному виду
    """

    def __init__(self, numerator, denominator):
        """
        Инициализация
        :param numerator: числитель (int, float или Fraction)
        :param denominator: знаменатель (int, float или Fraction)
        """
        if denominator == 0:
            raise FractionError('denominator = 0', {'def': '__init__', 'denominator': denominator})

        numerator_is_number = isinstance(numerator, int) or isinstance(numerator, float)
        denominator_is_number = isinstance(denominator, int) or isinstance(denominator, float)
        numerator_is_fraction = isinstance(numerator, Fraction)
        denominator_is_fraction = isinstance(denominator, Fraction)

        # Если числитель и знаменатель число
        if numerator_is_number and denominator_is_number:

            self.numerator = numerator
            self.denominator = denominator

        # Если числитель число, а знаменатель - дробь
        elif numerator_is_number and denominator_is_fraction:

            self.numerator = numerator * denominator.denominator
            self.denominator = denominator.numerator

        # Если числитель дробь, а знаменатель - число
        elif numerator_is_fraction and denominator_is_number:

            self.numerator = numerator.numerator
            self.denominator = numerator.denominator * denominator

        # Если числитель и знаменатель дробь
        elif numerator_is_fraction and denominator_is_fraction:

            self.numerator = numerator.numerator * denominator.denominator
            self.denominator = numerator.denominator * denominator.numerator

        else:
            raise FractionError('unknown type', {'def': '*', 'type_numenator': type(numerator),
                                                 'type_denominaor': type(denominator)})

    def reduction(self):
        """
        Раскладываем на простые множители и сокращаем
        :return: сокращенная дробь
        """
        numerator_positive = True
        if self.numerator < 0:
            numerator_positive = False

        prime_numbers_numerator = _factor(self.numerator)
        prime_numbers_denominator = _factor(self.denominator)
        prime_numbers_numerator, prime_numbers_denominator = _removing_identical_elements(prime_numbers_numerator,
                                                                                          prime_numbers_denominator)

        new_numerator = 1
        for elem in prime_numbers_numerator:
            new_numerator *= elem

        new_denominator = 1
        for elem in prime_numbers_denominator:
            new_denominator *= elem

        if not numerator_positive:
            new_numerator = -new_numerator

        if new_numerator / new_denominator == new_numerator // new_denominator:
            return new_numerator // new_denominator

        return Fraction(new_numerator, new_denominator)

    def __eq__(self, other):
        if isinstance(self, Fraction):
            self.reduction()
        if isinstance(other, Fraction):
            other.reduction()

        return self.numerator == other.numerator and self.denominator == other.denominator

    def __ne__(self, other):
        return self.numerator != other.numerator or self.denominator != other.denominator

    def __lt__(self, other):
        """
        Сравнение
        :param other: число или дробь
        :return: True - меньше, False - больше
        """
        if isinstance(other, int) and isinstance(other, float):
            return (self.numerator / self.denominator) < other
        elif isinstance(other, Fraction):
            # Одинаковые числители
            if self.numerator == other.numerator:
                return self.denominator > other.denominator
            # Одинаковые знаменатели
            elif self.denominator == other.denominator:
                return self.numerator < other.numerator
            # Разные числители и знаменатели
            else:
                prime_numbers1 = _factor(self.denominator)
                prime_numbers2 = _factor(other.denominator)
                prime_numbers1, prime_numbers2 = _removing_identical_elements(prime_numbers1, prime_numbers2)

                new_numerator1 = 1
                for elem in prime_numbers1:
                    new_numerator1 *= elem

                new_numerator2 = 1
                for elem in prime_numbers2:
                    new_numerator2 *= elem

                return prime_numbers1 < prime_numbers2

    def __add__(self, other):
        """
        Сложение
        :param other: то, с чем складываем (int, float или fraction)
        :return: результат сложения
        """

        result = Fraction(0, 1)
        if isinstance(other, int) or isinstance(other, float):
            result.numerator = self.numerator + other * self.denominator
            result.denominator = self.denominator
        elif isinstance(other, Fraction):
            result.numerator = self.numerator * other.denominator + other.numerator * self.denominator
            result.denominator = self.denominator * other.denominator
        else:
            raise FractionError('unknown type', {'def': '*', 'type': type(other)})

        return result.reduction()

    def __radd__(self, other):
        """
        Сложение
        :param other: то, с чем складываем (int, float или fraction)
        :return: результат сложения
        """

        result = Fraction(0, 1)
        if isinstance(other, int) or isinstance(other, float):
            result.numerator = self.numerator + other * self.denominator
            result.denominator = self.denominator
        elif isinstance(other, Fraction):
            result.numerator = self.numerator * other.denominator + other.numerator * self.denominator
            result.denominator = self.denominator * other.denominator
        else:
            raise FractionError('unknown type', {'def': '*', 'type': type(other)})

        return result.reduction()

    def __sub__(self, other):
        """
        Вычитание
        :param other: то, из чего вычитаем (int, float или fraction)
        :return: результат вычитания
        """

        result = Fraction(0, 1)
        if isinstance(other, int) or isinstance(other, float):
            result.numerator = self.numerator - other * self.denominator
            result.denominator = self.denominator
        elif isinstance(other, Fraction):
            result.numerator = self.numerator * other.denominator - other.numerator * self.denominator
            result.denominator = self.denominator * other.denominator
        else:
            raise FractionError('unknown type', {'def': '*', 'type': type(other)})

        return result.reduction()

    def __rsub__(self, other):
        """
        Вычитание
        :param other: то, что вычитаем (int, float или fraction)
        :return: результат вычитания
        """

        result = Fraction(0, 1)
        if isinstance(other, int) or isinstance(other, float):
            result.numerator = other * self.denominator - self.numerator
            result.denominator = self.denominator
        elif isinstance(other, Fraction):
            result.numerator = other.numerator * self.denominator - self.numerator * other.denominator
            result.denominator = self.denominator * other.denominator
        else:
            raise FractionError('unknown type', {'def': '*', 'type': type(other)})

        return result.reduction()

    def __mul__(self, other):
        """
        Умножение
        :param other: то, с чем умножаем (int, float или fraction)
        :return: результат умножения
        """

        result = Fraction(0, 1)
        if isinstance(other, int) or isinstance(other, float):
            result.numerator = self.numerator * other
            result.denominator = self.denominator
        elif isinstance(other, Fraction):
            result.numerator = self.numerator * other.numerator
            result.denominator = self.denominator * other.denominator
        else:
            raise FractionError('unknown type', {'def': '*', 'type': type(other)})

        return result.reduction()

    def __rmul__(self, other):
        """
        Умножение
        :param other: то, с чем умножаем (int, float или fraction)
        :return: результат умножения
        """

        result = Fraction(0, 1)
        if isinstance(other, int) or isinstance(other, float):
            result.numerator = self.numerator * other
            result.denominator = self.denominator
        elif isinstance(other, Fraction):
            result.numerator = self.numerator * other.numerator
            result.denominator = self.denominator * other.denominator
        else:
            raise FractionError('unknown type', {'def': '*', 'type': type(other)})

        return result.reduction()

    def __truediv__(self, other):
        """
        Деление
        :param other: то, на что делим (int, float или fraction)
        :return: результат деления
        """

        result = Fraction(0, 1)
        if isinstance(other, int) or isinstance(other, float):
            result.numerator = self.numerator
            result.denominator = self.denominator * other
        elif isinstance(other, Fraction):
            result.numerator = self.numerator * other.denominator
            result.denominator = self.denominator * other.numerator
        else:
            raise FractionError('unknown type', {'def': '*', 'type': type(other)})

        return result.reduction()

    def __rtruediv__(self, other):
        """
        Деление
        :param other: то, что делим (int, float или fraction)
        :return: результат деления
        """

        result = Fraction(0, 1)
        if isinstance(other, int) or isinstance(other, float):
            result.numerator = self.numerator
            result.denominator = self.denominator * other
        elif isinstance(other, Fraction):
            result.numerator = self.numerator * other.denominator
            result.denominator = self.denominator * other.numerator
        else:
            raise FractionError('unknown type', {'def': '*', 'type': type(other)})

        return result.reduction()

    def __floordiv__(self, other):
        """
        Целочисленное деление (в случае с дробью то же самое, что и обычное деление)
        :param other: то, на что делим (int, float или fraction)
        :return: результат деления
        """

        result = Fraction(0, 1)
        if isinstance(other, int) or isinstance(other, float):
            result.numerator = self.numerator
            result.denominator = self.denominator * other
        elif isinstance(other, Fraction):
            result.numerator = self.numerator * other.denominator
            result.denominator = self.denominator * other.numerator
        else:
            raise FractionError('unknown type', {'def': '*', 'type': type(other)})

        return result.reduction()

    def __rfloordiv__(self, other):
        """
        Целочисленное деление (в случае с дробью то же самое, что и обычное деление)
        :param other: то, что делим (int, float или fraction)
        :return: результат деления
        """

        result = Fraction(0, 1)
        if isinstance(other, int) or isinstance(other, float):
            result.numerator = self.numerator
            result.denominator = self.denominator * other
        elif isinstance(other, Fraction):
            result.numerator = self.numerator * other.denominator
            result.denominator = self.denominator * other.numerator
        else:
            raise FractionError('unknown type', {'def': '*', 'type': type(other)})

        return result.reduction()

    def __neg__(self):
        """
        Унарный минус
        :return: результат - объект Fraction
        """

        self.numerator = -self.numerator

        return self

    def __str__(self):
        """
        :return: Вывод дроби в виде 1/2
        """

        return '{}/{}'.format(self.numerator, self.denominator)

    def __repr__(self):
        """
        :return: Вывод дроби в виде 1/2
        """

        return '{}/{}'.format(self.numerator, self.denominator)
