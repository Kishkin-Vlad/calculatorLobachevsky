import unittest
from calculatorLobachevsky.polynom import _Monom, Polynom, PolynomError
from copy import deepcopy


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
        mon2 = _Monom(5, {'x': 1})
        self.assertEqual(mon1 < mon2, True)

        mon1 = _Monom(10, {'x': 1})
        mon2 = _Monom(1, {'x': 1, 'y': 2})
        self.assertEqual(mon1 < mon2, True)

        mon1 = _Monom(10, {'x': 1, 'y': 1})
        mon2 = _Monom(10, {'x': 1, 'y': 2})
        self.assertEqual(mon1 < mon2, True)

        mon1 = _Monom(10, {'y': 1, 'x': 1})
        mon2 = _Monom(10, {'x': 1, 'y': 2})
        self.assertEqual(mon1 < mon2, True)

        mon1 = _Monom(10, {'y': 1, 'x': 1})
        mon2 = _Monom(1, {'x': 1, 'y': 1})
        self.assertEqual(mon1 < mon2, False)

        mon1 = _Monom(10, {'x': 100, 'y': 50, 'z': 25})
        mon2 = _Monom(1, {'a': 1})
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

    def test_monom_gt_monom(self):
        """
        Сравнение мономов - >
        """

        mon1 = _Monom(10)
        mon2 = _Monom(20)
        self.assertEqual(mon1 > mon2, False)

        mon1 = _Monom(10)
        mon2 = _Monom(5, {'x': 1})
        self.assertEqual(mon1 > mon2, False)

        mon1 = _Monom(10, {'x': 1, 'y': 2})
        mon2 = _Monom(1, {'x': 1})
        self.assertEqual(mon1 > mon2, True)

        mon1 = _Monom(10, {'x': 1, 'y': 1})
        mon2 = _Monom(10, {'x': 1, 'y': 2})
        self.assertEqual(mon1 > mon2, False)

        mon1 = _Monom(10, {'y': 1, 'x': 1})
        mon2 = _Monom(10, {'x': 1, 'y': 2})
        self.assertEqual(mon1 > mon2, False)

        mon1 = _Monom(10, {'y': 1, 'x': 1})
        mon2 = _Monom(1, {'x': 1, 'y': 1})
        self.assertEqual(mon1 > mon2, True)

        mon1 = _Monom(10, {'x': 100, 'y': 50, 'z': 25})
        mon2 = _Monom(1, {'a': 1})
        self.assertEqual(mon1 > mon2, False)

    def test_monom_gt_number(self):
        """
        Сравнение монома и числа - >
        """

        mon = _Monom(10)
        num = 20
        self.assertEqual(mon > num, False)

        mon = _Monom(10)
        num = 10
        self.assertEqual(mon > num, False)

        mon = _Monom(5, {'x': 1})
        num = 10
        self.assertEqual(mon > num, True)

    def test_monom_ge_monom(self):
        """
        Сравнение мономов - >=
        """

        mon1 = _Monom(10)
        mon2 = _Monom(20)
        self.assertEqual(mon1 >= mon2, False)

        mon1 = _Monom(10)
        mon2 = _Monom(10, {'x': 1})
        self.assertEqual(mon1 >= mon2, False)

        mon1 = _Monom(10, {'x': 1})
        mon2 = _Monom(10, {'x': 1, 'y': 2})
        self.assertEqual(mon1 >= mon2, False)

        mon1 = _Monom(10, {'x': 1, 'y': 1})
        mon2 = _Monom(10, {'x': 1, 'y': 2})
        self.assertEqual(mon1 >= mon2, False)

        mon1 = _Monom(10, {'y': 2, 'x': 1})
        mon2 = _Monom(10, {'x': 1, 'y': 2})
        self.assertEqual(mon1 >= mon2, True)

    def test_monom_ge_number(self):
        """
        Сравнение монома и числа - >=
        """

        mon = _Monom(10)
        num = 20
        self.assertEqual(mon >= num, False)

        mon = _Monom(10)
        num = 10
        self.assertEqual(mon >= num, True)

        mon = _Monom(5, {'x': 1})
        num = 10
        self.assertEqual(mon >= num, True)

    def test_monom_mul(self):
        """
        Умножение типа = self * other, где other - число или моном
        """

        mon1 = _Monom(10)
        num = 10
        self.assertEqual((mon1 * num), 100)

        mon1 = _Monom(10)
        num = 10.1
        self.assertEqual((mon1 * num), 101)

        mon1 = _Monom(10)
        num = complex(10, 10)
        self.assertEqual((mon1 * num), complex(100, 100))

        mon1 = _Monom(10)
        mon2 = _Monom(20)
        self.assertEqual((mon1 * mon2), _Monom(200))

        mon1 = _Monom(10)
        mon2 = _Monom(20, {'x': 1})
        self.assertEqual((mon1 * mon2), _Monom(200, {'x': 1}))

        mon1 = _Monom(10, {'x': 1})
        mon2 = _Monom(20)
        self.assertEqual((mon1 * mon2), _Monom(200, {'x': 1}))

        mon1 = _Monom(10, {'x': 1})
        mon2 = _Monom(20, {'x': 2})
        self.assertEqual((mon1 * mon2), _Monom(200, {'x': 3}))

        mon1 = _Monom(10, {'x': 1})
        mon2 = _Monom(20, {'x': 2, 'y': 1})
        self.assertEqual((mon1 * mon2), _Monom(200, {'x': 3, 'y': 1}))

        mon1 = _Monom(10, {'x': 1, 'y': 1})
        mon2 = _Monom(20, {'x': 2})
        self.assertEqual((mon1 * mon2), _Monom(200, {'x': 3, 'y': 1}))

        mon1 = _Monom(10, {'x': 1, 'y': 4})
        mon2 = _Monom(20, {'x': 2, 'y': 3})
        self.assertEqual((mon1 * mon2), _Monom(200, {'x': 3, 'y': 7}))

        mon1 = _Monom(10, {'y': 4, 'x': 1})
        mon2 = _Monom(20, {'x': 2, 'y': 3})
        self.assertEqual((mon1 * mon2), _Monom(200, {'x': 3, 'y': 7}))

    def test_monom_rmul(self):
        """
        Умножение типа = other * self, где other - число или моном
        """

        mon1 = _Monom(10)
        num = 10
        self.assertEqual((num * mon1), 100)

        mon1 = _Monom(10)
        num = 10.1
        self.assertEqual((num * mon1), 101)

        mon1 = _Monom(10)
        num = complex(10, 10)
        self.assertEqual((num * mon1), complex(100, 100))

        mon1 = _Monom(10)
        mon2 = _Monom(20)
        self.assertEqual((mon2 * mon1), _Monom(200))

        mon1 = _Monom(10)
        mon2 = _Monom(20, {'x': 1})
        self.assertEqual((mon2 * mon1), _Monom(200, {'x': 1}))

        mon1 = _Monom(10, {'x': 1})
        mon2 = _Monom(20)
        self.assertEqual((mon2 * mon1), _Monom(200, {'x': 1}))

        mon1 = _Monom(10, {'x': 1})
        mon2 = _Monom(20, {'x': 2})
        self.assertEqual((mon2 * mon1), _Monom(200, {'x': 3}))

        mon1 = _Monom(10, {'x': 1})
        mon2 = _Monom(20, {'x': 2, 'y': 1})
        self.assertEqual((mon2 * mon1), _Monom(200, {'x': 3, 'y': 1}))

        mon1 = _Monom(10, {'x': 1, 'y': 1})
        mon2 = _Monom(20, {'x': 2})
        self.assertEqual((mon2 * mon1), _Monom(200, {'x': 3, 'y': 1}))

        mon1 = _Monom(10, {'x': 1, 'y': 4})
        mon2 = _Monom(20, {'x': 2, 'y': 3})
        self.assertEqual((mon2 * mon1), _Monom(200, {'x': 3, 'y': 7}))

        mon1 = _Monom(10, {'y': 4, 'x': 1})
        mon2 = _Monom(20, {'x': 2, 'y': 3})
        self.assertEqual((mon2 * mon1), _Monom(200, {'x': 3, 'y': 7}))

    def test_monom_imul(self):
        """
        Умножение типа self *= other, где other - число или моном
        """

        mon1 = _Monom(10)
        num = 10
        mon1 *= num
        self.assertEqual(mon1, 100)

        mon1 = _Monom(10)
        num = 10.1
        mon1 *= num
        self.assertEqual(mon1, 101)

        mon1 = _Monom(10)
        num = complex(10, 10)
        mon1 *= num
        self.assertEqual(mon1, complex(100, 100))

        mon1 = _Monom(10)
        mon2 = _Monom(20)
        mon1 *= mon2
        self.assertEqual(mon1, _Monom(200))

        mon1 = _Monom(10)
        mon2 = _Monom(20, {'x': 1})
        mon1 *= mon2
        self.assertEqual(mon1, _Monom(200, {'x': 1}))

        mon1 = _Monom(10, {'x': 1})
        mon2 = _Monom(20)
        mon1 *= mon2
        self.assertEqual(mon1, _Monom(200, {'x': 1}))

        mon1 = _Monom(10, {'x': 1})
        mon2 = _Monom(20, {'x': 2})
        mon1 *= mon2
        self.assertEqual(mon1, _Monom(200, {'x': 3}))

        mon1 = _Monom(10, {'x': 1})
        mon2 = _Monom(20, {'x': 2, 'y': 1})
        mon1 *= mon2
        self.assertEqual(mon1, _Monom(200, {'x': 3, 'y': 1}))

        mon1 = _Monom(10, {'x': 1, 'y': 1})
        mon2 = _Monom(20, {'x': 2})
        mon1 *= mon2
        self.assertEqual(mon1, _Monom(200, {'x': 3, 'y': 1}))

        mon1 = _Monom(10, {'x': 1, 'y': 4})
        mon2 = _Monom(20, {'x': 2, 'y': 3})
        mon1 *= mon2
        self.assertEqual(mon1, _Monom(200, {'x': 3, 'y': 7}))

        mon1 = _Monom(10, {'y': 4, 'x': 1})
        mon2 = _Monom(20, {'x': 2, 'y': 3})
        mon1 *= mon2
        self.assertEqual(mon1, _Monom(200, {'x': 3, 'y': 7}))

    def test_monom_add(self):
        """
        Сложение типа = self + other, где other - число или моном
        """

        mon1 = _Monom(10)
        mon2 = _Monom(20)
        self.assertEqual((mon1 + mon2), _Monom(30))

        mon1 = _Monom(3, {'x': 12})
        mon2 = _Monom(4, {'x': 12})
        self.assertEqual((mon1 + mon2), _Monom(7, {'x': 12}))

        mon1 = _Monom(3, {'x': 12})
        mon2 = _Monom(4)
        self.assertRaises(PolynomError, _Monom.__add__, mon1, mon2)

    def test_monom_iadd(self):
        """
        Сложение типа  self += other, где other - число или моном
        """

        mon1 = _Monom(10)
        mon2 = _Monom(20)
        mon1 += mon2
        self.assertEqual(mon1, _Monom(30))

        mon1 = _Monom(3, {'x': 12})
        mon2 = _Monom(4, {'x': 12})
        mon1 += mon2
        self.assertEqual(mon1, _Monom(7, {'x': 12}))

        mon1 = _Monom(3, {'x': 12})
        mon2 = _Monom(4)
        self.assertRaises(PolynomError, _Monom.__iadd__, mon1, mon2)

    def test_monom_str(self):
        """
        Преобразование монома к str
        """

        mon = _Monom(10, {'x': 10})
        self.assertEqual(str(mon), '10*x^10')

        mon = _Monom(20, {'x': 10, 'y': 20.5})
        self.assertEqual(str(mon), '20*x^10*y^20.5')

        mon = _Monom(20, {'x': 10, 'y': 20.5, 'abc12': complex(5, 2)})
        self.assertEqual(str(mon), '20*x^10*y^20.5*abc12^(5+2j)')

    def test_polynom_init(self):
        """
        Инициалиация полинома
        """

        pol1 = Polynom()

        pol2 = Polynom(10)

        mon = _Monom(10, {'x': 2, 'y': 3})
        pol3 = Polynom(mon)

        pol4 = Polynom(pol2 + pol3)

    def test_polynom_add(self):
        """
        Сложение полинома с числом/мономом/полиномом
        """

        mon1 = _Monom(10)
        mon2 = _Monom(5, {'x': 2})
        mon3 = _Monom(2, {'x': 3, 'y': 5})

        pol1 = Polynom()
        pol2 = Polynom()
        pol3 = Polynom()

        pol1 = pol1 + mon1
        pol2 = pol2 + mon2
        pol3 = pol3 + mon3
        self.assertEqual(pol1.list_monom[0], mon1)
        self.assertEqual(pol2.list_monom[0], mon2)
        self.assertEqual(pol3.list_monom[0], mon3)

        pol = Polynom()
        pol = pol + mon1
        pol = pol + mon2
        pol12 = pol1 + pol2
        self.assertEqual(pol.list_monom[0], pol12.list_monom[0])
        self.assertEqual(pol.list_monom[1], pol12.list_monom[1])

        pol = Polynom()
        pol = pol + mon1
        pol = pol + mon3
        pol13 = pol1 + pol3
        self.assertEqual(pol.list_monom[0], pol13.list_monom[0])
        self.assertEqual(pol.list_monom[1], pol13.list_monom[1])

        pol = Polynom()
        pol = pol + mon2
        pol = pol + mon3
        pol23 = pol2 + pol3
        self.assertEqual(pol.list_monom[0], pol23.list_monom[0])
        self.assertEqual(pol.list_monom[1], pol23.list_monom[1])

        pol = Polynom()
        pol = pol + mon1
        pol = pol + mon2
        pol = pol + mon3
        pol123 = pol1 + pol2 + pol3
        self.assertEqual(pol.list_monom[0], pol123.list_monom[0])
        self.assertEqual(pol.list_monom[1], pol123.list_monom[1])
        self.assertEqual(pol.list_monom[2], pol123.list_monom[2])

        pol = Polynom()
        pol = pol + 2 * mon1
        pol = pol + 2 * mon2
        pol = pol + 2 * mon3
        pol123 = pol1 + pol2 + pol3 + pol1 + pol2 + pol3
        self.assertEqual(pol.list_monom[0], pol123.list_monom[0])
        self.assertEqual(pol.list_monom[1], pol123.list_monom[1])
        self.assertEqual(pol.list_monom[2], pol123.list_monom[2])

        mon1 = _Monom(-10)
        mon2 = _Monom(-5, {'x': 2})
        mon3 = _Monom(-2, {'x': 3, 'y': 5})
        pol123 = pol1 + pol2
        pol123 = pol123 + pol3
        pol123 = pol123 + mon1
        pol123 = pol123 + mon2
        pol123 = pol123 + mon3
        self.assertEqual(pol123.list_monom[0], 0)

    def test_polynom_iadd(self):
        """
        Сложение полинома с числом/мономом/полиномом
        """

        mon1 = _Monom(10)
        mon2 = _Monom(5, {'x': 2})
        mon3 = _Monom(2, {'x': 3, 'y': 5})

        pol1 = Polynom()
        pol2 = Polynom()
        pol3 = Polynom()

        pol1 += mon1
        pol2 += mon2
        pol3 += mon3
        self.assertEqual(pol1.list_monom[0], mon1)
        self.assertEqual(pol2.list_monom[0], mon2)
        self.assertEqual(pol3.list_monom[0], mon3)

    def test_polynom_sub(self):
        """
        Разность полинома с числом/мономом/полиномом
        """

        mon1 = _Monom(10)
        mon2 = _Monom(5, {'x': 2})
        mon3 = _Monom(2, {'x': 3, 'y': 5})

        pol1 = Polynom()
        pol2 = Polynom()
        pol3 = Polynom()

        pol1 += mon1
        pol2 += mon2
        pol3 += mon3

        pol1 = pol1 - mon2
        self.assertEqual(pol1.list_monom[0], -mon2)
        self.assertEqual(pol1.list_monom[1], mon1)

        pol2 = pol2 - mon2
        self.assertEqual(pol2.list_monom[0], _Monom(0))

        pol3 = pol3 - mon1
        pol3 = pol3 - mon2
        self.assertEqual(pol3.list_monom[0], mon3)
        self.assertEqual(pol3.list_monom[1], -mon2)
        self.assertEqual(pol3.list_monom[2], -mon1)

    def test_polynom_isub(self):
        """
        Разность полинома с числом/мономом/полиномом
        """

        mon1 = _Monom(10)
        mon2 = _Monom(5, {'x': 2})
        mon3 = _Monom(2, {'x': 3, 'y': 5})

        pol1 = Polynom()
        pol2 = Polynom()
        pol3 = Polynom()

        pol1 += mon1
        pol2 += mon2
        pol3 += mon3

        pol1 -= mon2
        self.assertEqual(pol1.list_monom[0], -mon2)
        self.assertEqual(pol1.list_monom[1], mon1)

        pol2 -= mon2
        self.assertEqual(pol2.list_monom[0], _Monom(0))

        pol3 -= mon1
        pol3 -= mon2
        self.assertEqual(pol3.list_monom[0], mon3)
        self.assertEqual(pol3.list_monom[1], -mon2)
        self.assertEqual(pol3.list_monom[2], -mon1)

    def test_polynom_mul(self):
        """
        Умножение полинома на число/моном/полином
        """

        mon1 = _Monom(10)
        mon2 = _Monom(5, {'x': 2})
        mon3 = _Monom(2, {'x': 3, 'y': 5})

        pol1 = Polynom(mon1)
        pol2 = Polynom(mon2)
        pol3 = Polynom(mon3)

        pol4 = pol1 * 5
        self.assertEqual(pol4.list_monom[0], _Monom(50))

        pol5 = pol1 * mon2
        self.assertEqual(pol5.list_monom[0], _Monom(50, {'x': 2}))

        pol6 = pol2 * pol3
        self.assertEqual(pol6.list_monom[0], _Monom(10, {'x': 5, 'y': 5}))

    def test_polynom_imul(self):
        """
        Умножение полинома на число/моном/полином
        """

        mon1 = _Monom(10)
        mon2 = _Monom(5, {'x': 2})
        mon3 = _Monom(2, {'x': 3, 'y': 5})

        pol1 = Polynom(mon1)
        pol2 = Polynom(mon2)
        pol3 = Polynom(mon3)

        pol1 *= mon2
        self.assertEqual(pol1.list_monom[0], _Monom(50, {'x': 2}))

        pol2 *= pol3
        self.assertEqual(pol2.list_monom[0], _Monom(10, {'x': 5, 'y': 5}))

    def test_polynom_str(self):
        """
        Преобразование полинома к str
        """
        mon1 = _Monom(10)
        mon2 = _Monom(5, {'x': 2})
        mon3 = _Monom(2, {'x': 3, 'y': 5})

        pol1 = Polynom()
        pol2 = Polynom()
        pol3 = Polynom()

        pol1 = pol1 + mon1
        pol2 = pol2 + mon2
        pol3 = pol3 + mon3

        pol12 = pol1 + pol2
        self.assertEqual(str(pol12), '5*x^2+10')

        pol13 = pol1 + pol3
        self.assertEqual(str(pol13), '2*x^3*y^5+10')

        pol23 = pol2 + pol3
        self.assertEqual(str(pol23), '2*x^3*y^5+5*x^2')
