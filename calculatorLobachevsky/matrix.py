# Сторонние библиотеки
from copy import deepcopy


# Наши модули
from .polynom import Polynom
from .fraction import Fraction
from .Error import MatrixError


def _count_determinant(matrix: list):
    """
    Сам процесс получения определителя
    :param matrix: квадратная матрица
    :return: число (определитель)
    """

    determinant = 0
    len_matrix = len(matrix)
    # Для матрицы первого порядка
    if len_matrix == 1:
        return matrix[0][0]
    # Для матрицы второго порядка
    elif len_matrix == 2:
        determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    # Для матриц высшего порядка
    else:
        """
        Пробегаемся по первой строке матрицы умножая их на (-1)^... 
        и на дополнительные миноры квадратной матрицы
        """
        for col_count, number in enumerate(matrix[0]):
            mat = []
            for i, row_number in enumerate(matrix):
                # Всегда пропускаем первую строчку (чтобы правильно взять
                # дополнительные миноры)
                if i == 0:
                    continue

                mat.append([])
                for j, col_number in enumerate(matrix[i]):
                    # Пропускаем столбец, с которым работаем (чтобы правильно взять
                    # дополнительные миноры)
                    if col_count == j:
                        continue
                    mat[i - 1].append(col_number)

            """
            формула нахождения определителя в нашем случае:
            sum(a_(1)(col_count) * (-1)^(1 + col_count) * M), где
            sum - как математический знак E от 1 до количества столбцов в матрице
            a_(1)(col_count) - число из первой строки и столбца col_count
            1 - номер строки (у нас всегда первая строка)
            col_count - столбец, с которым работаем
            M - дополнительный минор для первой строки и столбца col_count
            """
            determinant += number * (-1) ** (2 + col_count) * _count_determinant(mat)

    return determinant


class Matrix(object):

    def __init__(self, matrix=None, row=None, col=None):
        """
        Инициализирует матрицу, передавая двумерный массив в виде [[], [], ..., []]
        или
        Инициализирует нулевую матрицу размера row x col
        :param matrix: матрица вида [[1,2,3], [2, 0]]
        :param row: количество строк
        :param col: количество столбцов
        """

        # Проверка на передаваемые типы параметров
        if not (isinstance(matrix, list) or matrix is None):
            raise MatrixError('matrix is not a two-dimensional array', {'def': '__init__',
                                                                        'matrix': matrix, 'type': type(matrix)})
        if not (isinstance(row, int) or row is None):
            raise MatrixError('row is not a int', {'def': '__init__', 'row': row, 'type': type(row)})
        if not (isinstance(col, int) or col is None):
            raise MatrixError('col is not a int', {'def': '__init__', 'col': col, 'type': type(col)})

        if matrix is not None:
            """
            Создаем матрицу вида matrix. Пример:
            Дана матрица:
            [ [1, 2, 3, 4],
              [5, 6],
              [7],
              [8, 9] ]
            Будет создана матрица:
            [ [1, 2, 3, 4],
              [5, 6, 0, 0],
              [7, 0, 0, 0],
              [8, 9, 0, 0] ]
            """
            arr_len = []
            rows = 0
            for row in matrix:
                arr_len.append(len(row))
                rows += 1
            cols = max(arr_len)
            del arr_len

            if cols == 0:
                raise MatrixError('a matrix of the form {}x0'.format(rows), {'def': '__init__', 'matrix': matrix})

            self.matrix = []
            for i_row, row in enumerate(matrix):
                self.matrix.append([])
                for col in range(cols):
                    try:
                        number = matrix[i_row][col]
                        if not (isinstance(number, int) or isinstance(number, float)):
                            raise MatrixError('an element in a matrix is not a number', {'def': '__init__',
                                                                                         'matrix': matrix})
                        self.matrix[i_row].append(number)
                    except IndexError:
                        self.matrix[i_row].append(0)

            self.row = rows
            self.col = cols
        elif not (row is None and col is None):
            # Создаем нулевую матрицу
            if row <= 0 or col <= 0:
                raise MatrixError('the parameters of row or col are less than or equal to zero',
                                  {'def': '__init__', 'row': row, 'col': col})

            self.matrix = []
            for i in range(row):
                self.matrix.append([])
                for j in range(col):
                    self.matrix[i].append(0)

            self.row = row
            self.col = col

    def __call__(self, matrix=None, row=None, col=None):
        """
        Пересоздаем в новую матрицу, передав двумерный массив в виде [[], [], ..., []]
        или
        Пересоздаем в нулевую матрицу размера row x col
        :param matrix: матрица вида [[1,2,3], [2, 0]]
        :param row: количество строк
        :param col: количество столбцов
        """

        # Проверка на передаваемые типы параметров
        if not (isinstance(matrix, list) or matrix is None):
            raise MatrixError('matrix is not a two-dimensional array', {'def': '__call__',
                                                                        'matrix': matrix, 'type': type(matrix)})
        if not (isinstance(row, int) or row is None):
            raise MatrixError('row is not a int', {'def': '__call__', 'row': row, 'type': type(row)})
        if not (isinstance(col, int) or col is None):
            raise MatrixError('col is not a int', {'def': '__call__', 'col': col, 'type': type(col)})

        if matrix is not None:
            """
            Создаем матрицу вида matrix. Пример:
            Дана матрица:
            [ [1, 2, 3, 4],
              [5, 6],
              [7],
              [8, 9] ]
            Будет создана матрица:
            [ [1, 2, 3, 4],
              [5, 6, 0, 0],
              [7, 0, 0, 0],
              [8, 9, 0, 0] ]
            """
            arr_len = []
            rows = 0
            for row in matrix:
                arr_len.append(len(row))
                rows += 1
            cols = max(arr_len)
            del arr_len

            if cols == 0:
                raise MatrixError('a matrix of the form {}x0'.format(rows), {'def': '__call__', 'matrix': matrix})

            self.matrix = []
            for i_row, row in enumerate(matrix):
                self.matrix.append([])
                for col in range(cols):
                    try:
                        number = matrix[i_row][col]
                        if not (isinstance(number, int) or isinstance(number, float)):
                            raise MatrixError('an element in a matrix is not a number', {'def': '__call__',
                                                                                         'matrix': matrix})
                        self.matrix[i_row].append(number)
                    except IndexError:
                        self.matrix[i_row].append(0)

            self.row = rows
            self.col = cols
        elif not (row is None and col is None):
            # Создаем нулевую матрицу
            if row <= 0 or col <= 0:
                raise MatrixError('the parameters of row or col are less than or equal to zero',
                                  {'def': '__call__', 'row': row, 'col': col})

            self.matrix = []
            for i in range(row):
                self.matrix.append([])
                for j in range(col):
                    self.matrix[i].append(0)

            self.row = row
            self.col = col

    def det(self):
        """
        Нахождение определителя квадратной матрицы
        :return: число (определитель)
        """

        if self.row != self.col:
            raise MatrixError('matrix is not square',
                              {'def': 'determinant', 'row': self.row, 'col': self.col})

        return _count_determinant(self.matrix)

    def transposition(self):
        """
        Транспонирование матрицы
        :return: транспонированная матрица
        """

        matrix = Matrix(row=self.col, col=self.row)
        for i in range(self.row):
            for j in range(self.col):
                matrix.matrix[j][i] = self.matrix[i][j]
        self.row, self.col = self.col, self.row

        return matrix

    def rank(self):
        """
        Считаем ранг матрицы
        Приводим к ступенчатому виду и считаем количество строк
        :return: ранг матрицы (int)
        """

        matrix = deepcopy(self)
        matrix.stepped_view()

        return matrix.row

    def tr(self):
        """
        Нахождение суммы главной элементов главной диагонали
        :return: сумма
        """

        if self.row != self.col:
            raise MatrixError('matrix is not square',
                              {'def': 'tr', 'row': self.row, 'col': self.col})

        total = 0
        for i in range(self.row):
            total += self.matrix[i][i]

        return total

    def stepped_view(self):
        """
        Приводим матрицу к ступенчатому виду
        :return: результат - объект Matrix ступенчатого вида
        """
        """
        Проходимся по матрице ровно столько, сколько строк
        каждый раз приводя строчку, с которой работаем, в вид [..., 1, ...]
        а все строчки ниже в вид [..., 0, ...]
        """

        # Сортируем матрицу для удобства и наглядности
        self.matrix.sort(reverse=True)

        i = 0
        while i < self.row:
            for count_row in range(i, self.row):
                """
                Преобразуем матрицу так, чтобы столбец,
                с которым работаем состоял из единиц, 
                начиная со строки i
                """

                """
                Если количество строк больше количества столбцов,
                и получилась матрица, например
                [ [1, 2],
                  [0, 1],
                  [0, 6],
                  [0, 7] ]
                и мы пытаясь взять элемент лежащий в 3 строке и
                в 3 столбце, получаем ошибку, то выходим из цикла
                """
                try:
                    number = self.matrix[count_row][i]
                except IndexError:
                    break

                if number == 1 or number == 0:
                    continue
                for j in range(i, self.col):
                    """
                    Чтобы получить единицы в нашем столбце, нужно
                    поделить все значения в столбце на значение, которое
                    сейчас в этих строчке и столбце
                    """

                    temp_num = Fraction(self.matrix[count_row][j], number)
                    self.matrix[count_row][j] = temp_num.reduction()

            """
            Сделаем матрицу более красивую
            если первый элемент в строке стоит с минусом,
            то умножим всю строку на -1
            """
            for row in range(i, self.row):
                """
                Если количество строк больше количества столбцов,
                и получилась матрица, например
                [ [1, 2],
                  [0, 1],
                  [0, 6],
                  [0, 7] ]
                и мы пытаясь взять элемент лежащий в 3 строке и
                в 3 столбце, получаем ошибку, то выходим из цикла
                """
                try:
                    if self.matrix[row][i] < 0:
                        for j in range(i, self.col):
                            self.matrix[row][j] = self.matrix[row][j] * (-1)
                except IndexError:
                    break

            if i != self.row - 1:
                for row_other in range(i + 1, self.row):
                    """
                    Вычитаем строку i из всех строк, ниже i
                    (так у нас во всем столбце 1, то ни
                    на что умножать строку i не нужно)                                
                    """

                    for col_other in range(i, self.col):
                        if self.matrix[row_other][col_other] != 0:
                            self.matrix[row_other][col_other] -= self.matrix[i][col_other]

            # Если текущая строка состоит только из 0,
            # то удаляем ее
            delete_row = True
            for temp_col in range(self.col):
                if self.matrix[i][temp_col] != 0:
                    delete_row = False
            if delete_row:
                self.matrix.pop(i)
                self.row -= 1

            i += 1

        """
        Если строк больше столбцов, то занулим все строки, что ниже
        последней обработанной нами строкой (а раз они зануляются в
        любом случае, то их нужно удалить)
        """
        if self.row > self.col:
            for count in range(self.row - self.col):
                self.matrix.pop(self.col)
                self.row -= 1

        """
        Т.к. могли удалиться первые элементы (единицы), то
        сделаем, чтобы строки начинались единиц
        """
        for i in range(self.row):
            unit = False
            number = 0
            for j in range(self.col):
                if self.matrix[i][j] != 0 and not unit:
                    unit = True
                    number = self.matrix[i][j]
                if unit:
                    self.matrix[i][j] /= number


        return self

    def gauss(self, decision: list):
        """
        Найти решение методом Гаусса
        :param :
        :return: массив решений, т. е. [x1, x2, ..., xn]
        """
        """
        Приводим матрицу к треульному виду и решаем систему уравнений
        """

        if len(decision) != self.row:
            raise MatrixError('the number of lines and the number of solutions passed do not match',
                              {'def': 'gauss', 'count rows': self.row, 'length decision': len(decision)})

        matrix = deepcopy(self.matrix)
        for i, elem in enumerate(decision):
            matrix[i].append(elem)
        matrix = Matrix(matrix)

        """
        Три разных состояния:
        1 - matrix.row + 1 == matrix.col: то есть матрица (допустим) будет 2х2 (квадратной) и справа столбец решений
        Для такой матрицы не будет свободных членов
        2 - matrix.row + 1 < matrix.col: то есть матрица  (допустим) будет минимум 2х3 и справа столбец решений
        Для такой матрица будет ровно self.col - self.row + 1 свободных членов
        3 - matrix.row + 1 > matrix.col: то есть матрица (допустим) будет 3х2 и справа стобец решений
        Для такой матрицы не будет свободных членов
        """
        if matrix.row + 1 == matrix.col:
            state = 1
        elif matrix.row + 1 < matrix.col:
            state = 2
        else:
            state = 3
        matrix.stepped_view()
        print(matrix)

        count = [matrix.row, True] if matrix.row <= matrix.col else [matrix.col, False]
        for i in range(count[0]):
            if matrix.matrix[i][i] == 0:
                matrix.matrix.pop(i)
                if count[1]:
                    matrix.row -= 1
                else:
                    matrix.col -= 1

        if state == 1 or state == 3:

            if state == 3:
                matrix.matrix.pop()
                matrix.row -= 1

            xns = []  # список всех Xn
            for i in range(matrix.row, 0, -1):  # идем в обратном порядке (от matrix.row до 0)
                # т.к. у нас число в [1][1], [2][2], ..., [n][n] всегда 1, то ничего делить не надо
                # (такие преобразования делает self.stepped_view())
                count_xn = matrix.row - i       # количество Xn, которые нужно будет подставлять
                xn = matrix.matrix[i - 1][-1]   # берем решение (правый элемент в этой строке)
                for x in range(count_xn):
                    # Вычитаем каждый член после [i][i] помноженный на коэф, который мы нашли ранее
                    # то есть для i = 3 и количества строк 5 найденные коэф - это X4, X5
                    xn -= matrix.matrix[i - 1][i + x] * xns[-(x + 1)]
                xns.append(xn)

        else:  # state == 2
            # Некорректно работает
            xns = []
            for i in range(matrix.row, 0, -1):  # идем в обратном порядке (от matrix.row до 0)
                # т.к. у нас число в [1][1], [2][2], ..., [n][n] всегда 1, то ничего делить не надо
                # (такие преобразования делает self.stepped_view())
                count_xn = matrix.row - i       # количество Xn, которые нужно будет подставлять
                if matrix.matrix[i - 1][i - 1] == 1:
                    xn = Polynom(matrix.matrix[i - 1][-1])   # берем решение (правый элемент в этой строке)
                elif matrix.matrix[i - 1][i - 1] == 0:
                    xn = Polynom(1, {'t': 1})
                for x in range(count_xn):
                    # Вычитаем каждый член после [i][i] помноженный на коэф, который мы нашли ранее
                    # то есть для i = 3 и количества строк 5 найденные коэф - это X4, X5
                    xn -= matrix.matrix[i - 1][i + x] * xns[-(x + 1)]
                xns.append(xn)

        return xns

    def __eq__(self, other):
        """
        Проверяем идентичны ли матрицы (==)
        :param other: матрица, с которой сравниваем
        :return: True - идентичны, False - не иденичны
        """

        if not isinstance(other, Matrix):
            raise MatrixError('type mismatch', {'def': '==', 'type1': type(self), 'type2':  type(other)})

        if len(self.matrix) != len(other.matrix):
            return False
        for val_our, val_other in zip(self.matrix, other.matrix):
            if val_our != val_other:
                return False

        return True

    def __ne__(self, other):
        """
        Проверяем не идентичны ли матрицы (!=)
        :param other: матрица, с которой сравниваем
        :return: True - не идентичны, False - иденичны
        """

        if not isinstance(other, Matrix):
            raise MatrixError('type mismatch', {'def': '==', 'type1': type(self), 'type2': type(other)})

        if len(self.matrix) != len(other.matrix):
            return True
        for val_our, val_other in zip(self.matrix, other.matrix):
            if val_our != val_other:
                return True

        return False

    def __add__(self, other):
        """
        Сумма двух объектов Matrix
        :param other: матрица, с которой суммируем
        :return: результат - объект Matrix
        """

        if not isinstance(other, Matrix):
            raise MatrixError('type mismatch', {'def': '==', 'type1': type(self), 'type2':  type(other)})

        if self.row != other.row:
            raise MatrixError('rows are not equal', {'def': '+', 'row1': self.row, 'row2': other.row})
        if self.col != other.col:
            raise MatrixError('rows are not equal', {'def': '+', 'col1': self.col, 'col2': other.col})

        matrix = Matrix(row=self.row, col=self.col)
        for i, (row1, row2) in enumerate(zip(self.matrix, other.matrix)):
            for j, (col1, col2) in enumerate(zip(row1, row2)):
                matrix.matrix[i][j] = col1 + col2

        return matrix

    def __iadd__(self, other):
        """
        Сумма двух объектов Matrix
        :param other: матрица, с которой суммируем
        :return: результат - объект Matrix
        """

        if not isinstance(other, Matrix):
            raise MatrixError('type mismatch', {'def': '==', 'type1': type(self), 'type2':  type(other)})

        if self.row != other.row:
            raise MatrixError('rows are not equal', {'def': '+', 'row1': self.row, 'row2': other.row})
        if self.col != other.col:
            raise MatrixError('rows are not equal', {'def': '+', 'col1': self.col, 'col2': other.col})

        for i, (row1, row2) in enumerate(zip(self.matrix, other.matrix)):
            for j, (col1, col2) in enumerate(zip(row1, row2)):
                self.matrix[i][j] = col1 + col2

        return self

    def __sub__(self, other):
        """
        Разность двух объектов Matrix
        :param other: матрица, к которой производим разность
        :return: результат - объект Matrix
        """

        if not isinstance(other, Matrix):
            raise MatrixError('type mismatch', {'def': '==', 'type1': type(self), 'type2':  type(other)})

        if self.row != other.row:
            raise MatrixError('rows are not equal', {'def': '-', 'row1': self.row, 'row2': other.row})
        if self.col != other.col:
            raise MatrixError('rows are not equal', {'def': '-', 'col1': self.col, 'col2': other.col})

        matrix = Matrix(row=self.row, col=self.col)
        for i, (row1, row2) in enumerate(zip(self.matrix, other.matrix)):
            for j, (col1, col2) in enumerate(zip(row1, row2)):
                matrix.matrix[i][j] = col1 - col2

        return matrix

    def __isub__(self, other):
        """
        Разность двух объектов Matrix
        :param other: матрица, к которой производим разность
        :return: результат - объект Matrix
        """

        if not isinstance(other, Matrix):
            raise MatrixError('type mismatch', {'def': '==', 'type1': type(self), 'type2':  type(other)})

        if self.row != other.row:
            raise MatrixError('rows are not equal', {'def': '-', 'row1': self.row, 'row2': other.row})
        if self.col != other.col:
            raise MatrixError('rows are not equal', {'def': '-', 'col1': self.col, 'col2': other.col})

        for i, (row1, row2) in enumerate(zip(self.matrix, other.matrix)):
            for j, (col1, col2) in enumerate(zip(row1, row2)):
                self.matrix[i][j] = col1 - col2

        return self

    def __neg__(self):
        """
        Унарный минус (ко всем числам в матрице применяется *(-1))
        :return: результат - объект Matrix
        """
        
        for i, row in enumerate(self.matrix):
            for j, col in enumerate(row):
                self.matrix[i][j] = -1 * col
            
        return self

    def __mul__(self, other):
        """
        Произведение двух объектов Matrix
        :param other: матрица, к которой производим умножение или число
        :return: результат - объект Matrix
        """

        if isinstance(other, Matrix):
            if self.col != other.row:
                raise MatrixError('the number of columns in the first matrix is not equal'
                                  ' to the number of rows in the second matrix',
                                  {'def': '*', 'col_matrix1': self.col, 'row_matrix2': other.row})

            matrix = Matrix(row=self.row, col=other.col)
            for row in range(self.row):
                for col in range(other.col):
                    for row_col in range(self.col):
                        matrix.matrix[row][col] += self.matrix[row][row_col] * other.matrix[row_col][col]

            return matrix

        elif isinstance(other, int) or isinstance(other, float):
            matrix = Matrix(row=self.row, col=self.col)
            for i in range(self.row):
                for j in range(self.col):
                    matrix.matrix[i][j] *= other

            return matrix
        else:
            raise MatrixError('raw types for multiplication', {'def': '*', 'type1': type(self), 'type': type(other)})

    def __rmul__(self, other):
        """
        Произведение двух объектов Matrix
        :param other: матрица, к которой производим умножение или число
        :return: результат - объект Matrix
        """

        if isinstance(other, Matrix):
            if self.col != other.row:
                raise MatrixError('the number of columns in the first matrix is not equal'
                                  ' to the number of rows in the second matrix',
                                  {'def': '*', 'col_matrix1': self.col, 'row_matrix2': other.row})

            matrix = Matrix(row=other.row, col=self.col)
            for row in range(other.row):
                for col in range(self.col):
                    for row_col in range(other.col):
                        matrix.matrix[row][col] += other.matrix[row][row_col] * self.matrix[row_col][col]

            return matrix

        elif isinstance(other, int) or isinstance(other, float):
            matrix = Matrix(row=self.row, col=self.col)
            for i in range(self.row):
                for j in range(self.col):
                    matrix.matrix[i][j] *= other

            return matrix
        else:
            raise MatrixError('raw types for multiplication', {'def': '*', 'type1': type(self), 'type': type(other)})

    def __imul__(self, other):
        """
        Произведение двух объектов Matrix
        :param other: матрица, к которой производим умножение или число
        :return: результат - объект Matrix
        """

        if isinstance(other, Matrix):
            if self.col != other.row:
                raise MatrixError('the number of columns in the first matrix is not equal'
                                  ' to the number of rows in the second matrix',
                                  {'def': '*', 'col_matrix1': self.col, 'row_matrix2': other.row})

            matrix = Matrix(row=self.row, col=other.col)
            for row in range(self.row):
                for col in range(other.col):
                    for row_col in range(self.col):
                        matrix.matrix[row][col] += self.matrix[row][row_col] * other.matrix[row_col][col]

            return matrix

        elif isinstance(other, int) or isinstance(other, float):
            for i in range(self.row):
                for j in range(self.col):
                    self.matrix[i][j] *= other

            return self
        else:
            raise MatrixError('raw types for multiplication', {'def': '*', 'type1': type(self), 'type': type(other)})

    def __bool__(self):
        """
        Проверка вырожденная матрица или нет
        :return: True - вырождена, False - не вырождена
        """

        return not self.det()

    def __str__(self):
        """
        :return: Вывод матрицы в виде (пример матрица 3x2):
         [ [0, 0],
           [0, 0],
           [0, 0] ]
        """

        result = '['
        for i in range(self.row):
            if i == 0:
                result = '{} {},'.format(result, str(self.matrix[i]))
            else:
                result = '{}  {},'.format(result, str(self.matrix[i]))
            result = '{}\n'.format(result)
        result = '{} ]'.format(result[:-2])

        return result

    def __repr__(self):
        """
        :return: Вывод матрицы в виде (пример матрица 3x2): [[0, 0], [0, 0], [0, 0]]
        """

        return str(self.matrix)
