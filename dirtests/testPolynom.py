import unittest
from calculatorLobachevsky.polynom import _Monom, Polynom, PolynomError


class TestPolynom(unittest.TestCase):

    def test_init_numbers(self):
        """
        Инициализация чисел
        """

        _Monom(1)
        _Monom(1.0)
        _Monom(complex(1, 2))

    def test_init_with_variables(self):
        """
        Инициализация с переменными
        """

        _Monom(2, {'x': 1})
        _Monom(3, {'y': 2, 'z': 3})
        _Monom(10, {'param1': 20, 'param2': 30})

    def test_init_number_with_error(self):
        """
        Попытка инициализировать число с передачей не числа
        """

        self.assertRaises(PolynomError, _Monom.__init__, self, '10')
        self.assertRaises(PolynomError, _Monom.__init__, self, [10])
        self.assertRaises(PolynomError, _Monom.__init__, self, {10: 20})

    def test_get_coef(self):
        """
        Получение коэффициента
        """

        monom = _Monom(10, {'x': 1, 'y': 2})
        self.assertEqual(monom.get_coefficient(), 10)

        monom = _Monom(20)
        self.assertEqual(monom.get_coefficient(), 20)

    def test_get_power(self):
        """
        Получение степени переменных
        """

        monom = _Monom(1, {'x': 2, 'y': 3})
        self.assertEqual(monom.get_power('x'), 2)
        self.assertEqual(monom.get_power('y'), 3)
        self.assertEqual(monom.get_power(['x', 'y']), [2, 3])

    def test_get_power_with_error(self):
        """
        Попытка получить переменных, которых нет
        """

        monom = _Monom(1, {'x': 2})
        self.assertRaises(PolynomError, _Monom.get_power, monom, 'y')
        self.assertRaises(PolynomError, _Monom.get_power, monom, ['x', 'y'])
        self.assertRaises(PolynomError, _Monom.get_power, monom, ['y', 'z'])
        self.assertRaises(PolynomError, _Monom.get_power, monom, 1)

    def test_monom_equal_monom(self):
        """
        Проверка равенства мономов
        """

        mon1 = _Monom(10)
        mon2 = _Monom(10)
        self.assertEqual(mon1, mon2)

        mon1 = _Monom(10, {'x': 1})
        mon2 = _Monom(10, {'x': 1})
        self.assertEqual(mon1, mon2)

        mon1 = _Monom(10, {'x': 1, 'y': 2})
        mon2 = _Monom(10, {'y': 2, 'x': 1})
        self.assertEqual(mon1, mon2)

    def test_monom_not_equal_monom(self):
        """
        Проверка неравенства мономов
        """

        mon1 = _Monom(10)
        mon2 = _Monom(20)
        self.assertNotEqual(mon1, mon2)

        mon1 = _Monom(10)
        mon2 = _Monom(10, {'x': 1})
        self.assertNotEqual(mon1, mon2)

    def test_monom_equal_numbers(self):
        """
        Проверка равенства монома и числа
        """

        mon = _Monom(10)
        num = 10
        self.assertEqual(mon, num)

        mon = _Monom(20.5)
        num = 20.5
        self.assertEqual(mon, num)

        mon = _Monom(30)
        num = complex(30, 0)
        self.assertEqual(mon, num)

    def test_monom_not_equal_numbers(self):
        """
        Проверка неравенства монома и числа
        """

        mon = _Monom(10)
        num = 20
        self.assertNotEqual(mon, num)

        mon = _Monom(10.1)
        num = _Monom(10.2)
        self.assertNotEqual(mon, num)

        mon = _Monom(10)
        num = complex(10, 1)
        self.assertNotEqual(mon, num)

        mon = _Monom(10, {'x': 1})
        num = _Monom(10)
        self.assertNotEqual(mon, num)

    def test_monom_lt_monom(self):
        """
        Сравнение мономов - <
        """

        mon1 = _Monom(10)
        mon2 = _Monom(20)
        self.assertEqual(mon1 < mon2, True)

        mon1 = _Monom(10)
        mon2 = _Monom(10, {'x': 1})
        self.assertEqual(mon1 < mon2, True)

        mon1 = _Monom(10, {'x': 1})
        mon2 = _Monom(10, {'x': 1, 'y': 2})
        self.assertEqual(mon1 < mon2, True)

        mon1 = _Monom(10, {'x': 1, 'y': 1})
        mon2 = _Monom(10, {'x': 1, 'y': 2})
        self.assertEqual(mon1 < mon2, True)

        mon1 = _Monom(10, {'y': 1, 'x': 1})
        mon2 = _Monom(10, {'x': 1, 'y': 2})
        self.assertEqual(mon1 < mon2, True)

    def test_monom_lt_number(self):
        """
        Сравнение монома и числа - <
        """

        mon = _Monom(10)
        num = 20
        self.assertEqual(mon < num, True)

        mon = _Monom(10)
        num = 10
        self.assertEqual(mon < num, False)

        mon = _Monom(5, {'x': 1})
        num = 10
        self.assertEqual(mon < num, False)

    def test_monom_le_monom(self):
        """
        Сравнение мономов - <=
        """

        mon1 = _Monom(10)
        mon2 = _Monom(20)
        self.assertEqual(mon1 <= mon2, True)

        mon1 = _Monom(10)
        mon2 = _Monom(10, {'x': 1})
        self.assertEqual(mon1 <= mon2, True)

        mon1 = _Monom(10, {'x': 1})
        mon2 = _Monom(10, {'x': 1, 'y': 2})
        self.assertEqual(mon1 <= mon2, True)

        mon1 = _Monom(10, {'x': 1, 'y': 1})
        mon2 = _Monom(10, {'x': 1, 'y': 2})
        self.assertEqual(mon1 <= mon2, True)

        mon1 = _Monom(10, {'y': 2, 'x': 1})
        mon2 = _Monom(10, {'x': 1, 'y': 2})
        self.assertEqual(mon1 <= mon2, True)

    def test_monom_le_number(self):
        """
        Сравнение монома и числа - <=
        """

        mon = _Monom(10)
        num = 20
        self.assertEqual(mon <= num, True)

        mon = _Monom(10)
        num = 10
        self.assertEqual(mon <= num, True)

        mon = _Monom(5, {'x': 1})
        num = 10
        self.assertEqual(mon <= num, False)
