# Сторонние библиотеки
# Испортируем очередь
from collections import deque


# Наши модули
from Error import ExpressionError


# Типы встречаемых символов (type element)
# 0 - 'value' число
# 1 - 'var' параметр
# 2 - 'bin_operator' бинарный оператор
# 3 - 'unary_operator' унарный оператор
# 4 - 'l_bracket' левая скобка
# 5 - 'r_bracket' правая скобка

# Состояния для анализа (state)
# 0 - унарный минус или не известно что (начало или начало после '(')
# 1 - число
# 2 - параметр или правая скобка
# 3 - операторы +, -, *, /, ^


class _Lexem(object):

    def __init__(self, expression: str, type_element, value=-1.0, priority=-1):
        """
        Инициализация
        :param expression: само выражение (строка)
        :param type_element: тип лексемы
        :param value: значение (для чисел)
        :param priority: приоритет
        """

        self.str = expression
        self.type_element = type_element
        self.value = value
        self.priority = priority

    def get_str(self):
        return self.str

    def get_type_element(self):
        return self.type_element

    def get_value(self):
        return self.value

    def get_priority(self):
        return self.priority

    def __eq__(self, other):
        if isinstance(other, _Lexem):
            return self.str == other.str and self.type_element == other.type_element and \
                   self.value == other.value and self.priority == other.priority

    def __repr__(self):
        return self.str

    def __str__(self):
        return self.str


class Expression(object):

    def __init__(self, expression: str):
        """
        Инициализация
        :param expression: само выражение (строка)
        """

        self.__input_expression = expression
        self.__output_expression = ''
        self.__vars = {}
        self.__listRPN = deque()

    def __lex_analysis(self):
        """
        Лексический анализ выражения
        Разбиваем нашу строку на лексемы и записываем our_list
        :return: список c лексемами
        """

        our_list = deque()
        self.__input_expression = '{} '.format(self.__input_expression.replace(' ', ''))
        if self.__input_expression == ' ':
            raise ExpressionError('empty expression', {'def': '__lex_analysis (Lexical Analysis)'})

        lex = ''
        state = 0
        count_brackets = 0
        temp_ch = ''

        for i, char in enumerate(self.__input_expression):
            if state == 0:
                """
                унарный минус или не известно что (начало или начало после '(')
                """

                lex = char

                if '0' <= char <= '9':
                    state = 1
                elif 'a' <= char <= 'z':
                    state = 2
                elif char == '-':
                    state = 3
                    our_list.append(_Lexem(lex, 3))
                elif char == '(':
                    count_brackets += 1
                    our_list.append(_Lexem(lex, 4))
                elif char == ')':
                    state = 2

                    count_brackets -= 1
                    if count_brackets < 0:
                        raise ExpressionError('count left and right brackets not the same',
                                              {'def': '__lex_analysis (Lexical Analysis)'})

                    our_list.append(_Lexem(lex, 5))
                elif char == ' ':
                    pass
                elif char == '+' or char == '^' or char == '*' or char == '/':
                    raise ExpressionError('expression is invalid - binary operation is in the wrong place',
                                          {'def': '__lex_analysis (Lexical Analysis)', 'char': char})
                else:
                    raise ExpressionError('expression is invalid - incorrect character',
                                          {'def': '__lex_analysis (Lexical Analysis)', 'char': char})

            elif state == 1:
                """
                число
                """

                if '0' <= char <= '9':
                    lex += char
                else:
                    our_list.append(_Lexem(lex, 0, float(lex)))

                    state = 3
                    lex = char
                    if char == '+' or char == '-':
                        our_list.append(_Lexem(lex, 2, -1, 1))
                    elif char == '*' or char == '/':
                        our_list.append(_Lexem(lex, 2, -1, 2))
                    elif char == '^':
                        our_list.append(_Lexem(lex, 2, -1, 3))
                    elif 'a' <= char <= 'z':
                        state = 2

                        our_list.append(_Lexem('*', 2, -1, 2))
                    elif char == '(':
                        state = 0

                        count_brackets += 1
                        our_list.append(_Lexem('*', 2, -1, 2))
                        our_list.append(_Lexem(lex, 4))
                    elif char == ')':
                        state = 2

                        count_brackets -= 1
                        if count_brackets < 0:
                            raise ExpressionError('count left and right brackets not the same',
                                                  {'def': '__lex_analysis (Lexical Analysis)'})

                        our_list.append(_Lexem(lex, 5))
                    elif char == ' ':
                        pass
                    else:
                        raise ExpressionError('expression is invalid - incorrect character',
                                              {'def': '__lex_analysis (Lexical Analysis)', 'char': char})

            elif state == 2:
                """
                параметр или )
                """

                # Если последний элемент )
                if our_list and our_list[-1].get_type_element() == 5:
                    lex = char

                    if '1' <= char <= '9':
                        state = 1

                        our_list.append(_Lexem('*', 2, -1, 2))
                    elif 'a' <= char <= 'z':
                        our_list.append(_Lexem('*', 2, -1, 2))
                    elif char == '+' or char == '-':
                        state = 3

                        our_list.append(_Lexem(lex, 2, -1, 1))
                    elif char == '*' or char == '/':
                        state = 3

                        our_list.append(_Lexem(lex, 2, -1, 2))
                    elif char == '^':
                        state = 3

                        our_list.append(_Lexem(lex, 2, -1, 3))
                    elif char == '(':
                        state = 0

                        count_brackets += 1
                        our_list.append(_Lexem('*', 2, -1, 2))
                        our_list.append(_Lexem(lex, 4))
                    elif char == ')':
                        state = 2

                        count_brackets -= 1
                        if count_brackets < 0:
                            raise ExpressionError('count left and right brackets not the same',
                                                  {'def': '__lex_analysis (Lexical Analysis)'})

                        our_list.append(_Lexem(lex, 5))
                    elif char == ' ':
                        pass
                    else:
                        raise ExpressionError('expression is invalid - incorrect character',
                                              {'def': '__lex_analysis (Lexical Analysis)', 'char': char})
                # Если число или переменная
                else:
                    if '1' <= char <= '9':
                        """
                        temp_ch нужен для отлова ошибок типа <буквы><числа> (для переменных)
                        Как можно писать переменную: a, a1, param1234
                        Как нельзя: a1a, param1from
                        """
                        temp_ch = char
                        lex = char
                    elif 'a' <= char <= 'z':
                        if '1' <= temp_ch <= '9':
                            raise ExpressionError('how should it look var: <letters><number>'
                                                  ' (the number can be omitted)',
                                                  {'def': '__lex_analysis (Lexical Analysis)', 'variable': lex,
                                                   'variable+char': '{}{}'.format(lex, char)})
                        lex += char
                    elif char == '+' or char == '-':
                        state = 3

                        if lex not in self.__vars.keys():
                            self.__vars[lex] = None
                        our_list.append(_Lexem(lex, 1))

                        lex = char
                        our_list.append(_Lexem(lex, 2, -1, 1))
                    elif char == '*' or char == '/':
                        state = 3

                        if lex not in self.__vars.keys():
                            self.__vars[lex] = None
                        our_list.append(_Lexem(lex, 1))

                        lex = char
                        our_list.append(_Lexem(lex, 2, -1, 2))
                    elif char == '^':
                        state = 3

                        if lex not in self.__vars.keys():
                            self.__vars[lex] = None
                        our_list.append(_Lexem(lex, 1))

                        lex = char
                        our_list.append(_Lexem(lex, 2, -1, 3))
                    elif char == '(':
                        state = 0
                        count_brackets += 1

                        if lex not in self.__vars.keys():
                            self.__vars[lex] = None
                        our_list.append(_Lexem(lex, 1))

                        lex = char
                        our_list.append(_Lexem(lex, 4))
                    elif char == ')':
                        state = 2

                        count_brackets -= 1
                        if count_brackets < 0:
                            raise ExpressionError('count left and right brackets not the same',
                                                  {'def': '__lex_analysis (Lexical Analysis)'})

                        if lex not in self.__vars.keys():
                            self.__vars[lex] = None
                        our_list.append(_Lexem(lex, 1))

                        lex = char
                        our_list.append(_Lexem(lex, 5))
                    elif char == ' ':
                        state = 0

                        if lex not in self.__vars.keys():
                            self.__vars[lex] = None
                        our_list.append(_Lexem(lex, 1))
                    else:
                        raise ExpressionError('expression is invalid - incorrect character',
                                              {'def': '__lex_analysis (Lexical Analysis)', 'char': char})

            elif state == 3:
                """
                операторы +, -, *, /, ^
                """

                lex = char

                if '0' <= char <= '9':
                    state = 1
                elif 'a' <= char <= 'z':
                    state = 2
                elif char == '-':
                    our_list.append(_Lexem(lex, 3,))
                elif char == '(':
                    state = 0

                    count_brackets += 1
                    our_list.append(_Lexem(lex, 4))
                elif char == ')':
                    state = 2

                    count_brackets -= 1
                    if count_brackets < 0:
                        raise ExpressionError('count left and right brackets not the same',
                                              {'def': '__lex_analysis (Lexical Analysis)'})
                    our_list.append(_Lexem(lex, 5))
                elif char == ' ':
                    pass
                elif char == '+' or char == '^' or char == '*' or char == '/':
                    raise ExpressionError('expression is invalid - binary operation is in the wrong place',
                                          {'def': '__lex_analysis (Lexical Analysis)', 'char': char})
                else:
                    raise ExpressionError('expression is invalid - incorrect character',
                                          {'def': '__lex_analysis (Lexical Analysis)', 'char': char})

        if count_brackets != 0:
            raise ExpressionError('count left and right brackets not the same',
                                  {'def': '__lex_analysis (Lexical Analysis)'})

        return our_list

    def __sync_analysis(self, in_list):
        """
        Синтаксический анализ
        :return: готовый список для вычисления
        """

        stack = deque()
        out_list = deque()
        for lex in in_list:
            type_elem = lex.get_type_element()
            # число или параметр
            if type_elem == 0 or type_elem == 1:
                out_list.append(lex)
            # бинарная операция
            elif type_elem == 2:
                prior = lex.get_priority()
                if stack:
                    prior_top_elem = stack[-1].get_priority()
                    if prior < prior_top_elem:
                        while stack:
                            out_list.append(stack.pop())
                stack.append(lex)
                # унарный оператор
            elif type_elem == 3:
                stack.append(lex)
            # левая скобка
            elif type_elem == 4:
                stack.append(lex)
            # правая скобка
            else:
                temp_te = stack[-1].get_type_element()
                while temp_te != 4:
                    out_list.append(stack.pop())
                    temp_te = stack[-1].get_type_element()
                stack.pop()

        # выгружаем все, что осталось, из стека
        while stack:
            out_list.append(stack.pop())

        return out_list

    def clear(self, expression: str):
        """
        Запись нового выражения
        :param expression: само выражение (строка)
        """
        self.__input_expression = expression
        self.__output_expression = ''
        self.__vars = {}
        self.__listRPN = deque()

    def get_input_expression(self):
        return self.__input_expression

    def get_output_expression(self):
        return self.__output_expression

    def add_var(self, var):
        """
        Добавление значений к переменным
        :param var: словарь с:
        ключами - имена переменных
        значениями - значения переменных
        """

        temp = var
        keys = temp.keys()
        for key in keys:
            self.__vars[key] = var[key]

    def __convert_to_rev_pol_not(self):
        """
        Перевод в обратную польскую запись
        """
        if self.__input_expression == '':
            raise ExpressionError('expression is not initialized', {'def': 'convert_to_rev_pol_not'})

        in_list = self.__lex_analysis()

        self.__listRPN = self.__sync_analysis(in_list)
        del in_list

        for elem in self.__listRPN:
            self.__output_expression += elem.get_str()

    def calculate(self):
        """
        Считает обратную польскую запись
        :return: число, которое последнее осталось после ОПЗ
        """

        self.__convert_to_rev_pol_not()
        stack = deque()
        for lex in self.__listRPN:
            type_elem = lex.get_type_element()
            # для чисел
            if type_elem == 0:
                stack.append(lex)
            # для переменных
            elif type_elem == 1:
                stack.append(_Lexem(lex.get_str(), 0, self.__vars[lex.get_str()]))
            # для бинарных операций
            elif type_elem == 2:
                elem2 = stack.pop()
                elem1 = stack.pop()

                if lex.get_str() == '+':
                    val = elem1.get_value() + elem2.get_value()
                    stack.append(_Lexem(str(val), 0, val))
                elif lex.get_str() == '-':
                    val = elem1.get_value() - elem2.get_value()
                    stack.append(_Lexem(str(val), 0, val))
                elif lex.get_str() == '*':
                    val = elem1.get_value() * elem2.get_value()
                    stack.append(_Lexem(str(val), 0, val))
                elif lex.get_str() == '/':
                    if elem2.get_value() == 0:
                        raise ExpressionError('in calculations, it turns out to be 0', {'def': 'calculate_expression'})

                    val = elem1.get_value() / elem2.get_value()
                    stack.append(_Lexem(str(val), 0, val))
                else:
                    val = elem1.get_value() ** elem2.get_value()
                    stack.append(_Lexem(str(val), 0, val))
            # для унарных операций
            else:
                elem = stack.pop()
                val = - elem.get_value()

                stack.append(_Lexem(str(val), 0, val))

        num = stack.pop().get_value()

        if num == int(num):
            return int(num)
        return num
