# Наши модули
from Error import *


def _count_datermint(matrix: list):
    """
    Сам процесс получения определителя
    :param matrix: квадратная матрица
    :return: число (определитель)
    """

    datermint = 0
    len_matrix = len(matrix)
    # Для матрицы первого порядка
    if len_matrix == 1:
        return matrix[0][0]
    # Для матрицы второго порядка
    elif len_matrix == 2:
        datermint = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
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

            # формула нахождения определителя в нашем случае:
            # sum(a_(1)(col_count) * (-1)^(1 + col_count) * M), где
            # sum - как математический знак E от 1 до количества столбцов в матрице
            # a_(1)(col_count) - число из первой строки и столбца col_count
            # 1 - номер строки (у нас всегда первая строка)
            # col_count - столбец, с которым работаем
            # M - дополнительный минор для первой строки и столбца col_count
            datermint += number * (-1) ** (2 + col_count) * _count_datermint(mat)

    return datermint


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
            raise MatrixError('matrix is not a two-dimensional array', {'matrix': matrix, 'type': type(matrix)})
        if not (isinstance(row, int) or row is None):
            raise MatrixError('row is not a int', {'row': row, 'type': type(row)})
        if not (isinstance(col, int) or col is None):
            raise MatrixError('col is not a int', {'col': col, 'type': type(col)})

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
                raise MatrixError('a matrix of the form {}x0'.format(rows), {'matrix': matrix})

            self.matrix = []
            for i_row, row in enumerate(matrix):
                self.matrix.append([])
                for col in range(cols):
                    try:
                        number = matrix[i_row][col]
                        if not (isinstance(number, int) or isinstance(number, float)):
                            raise MatrixError('an element in a matrix is not a number', {'matrix': matrix})
                        self.matrix[i_row].append(number)
                    except IndexError:
                        self.matrix[i_row].append(0)

            self.row = rows
            self.col = cols
        elif not (row is None and col is None):
            # Создаем нулевую матрицу
            if row <= 0 or col <= 0:
                raise MatrixError('the parameters of row or col are less than or equal to zero',
                                  {'row': row, 'col': col})

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
            raise MatrixError('matrix is not a two-dimensional array', {'matrix': matrix, 'type': type(matrix)})
        if not (isinstance(row, int) or row is None):
            raise MatrixError('row is not a int', {'row': row, 'type': type(row)})
        if not (isinstance(col, int) or col is None):
            raise MatrixError('col is not a int', {'col': col, 'type': type(col)})

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
                raise MatrixError('a matrix of the form {}x0'.format(rows), {'matrix': matrix})

            self.matrix = []
            for i_row, row in enumerate(matrix):
                self.matrix.append([])
                for col in range(cols):
                    try:
                        number = matrix[i_row][col]
                        if not (isinstance(number, int) or isinstance(number, float)):
                            raise MatrixError('an element in a matrix is not a number', {'matrix': matrix})
                        self.matrix[i_row].append(number)
                    except IndexError:
                        self.matrix[i_row].append(0)

            self.row = rows
            self.col = cols
        elif not (row is None and col is None):
            # Создаем нулевую матрицу
            if row <= 0 or col <= 0:
                raise MatrixError('the parameters of row or col are less than or equal to zero',
                                  {'row': row, 'col': col})

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

        return _count_datermint(self.matrix)

    def transposition(self):
        """
        Транспонирование матрицы
        :return: транспонированная матрица
        """

        matrix = Matrix(row=self.col, col=self.row)
        for i in range(self.row):
            for j in range(self.col):
                matrix.matrix[j][i] = self.matrix[i][j]

        return matrix

    # x < y
    def __lt__(self, other):
        pass

    # x <= y
    def __le__(self, other):
        pass

    def __eq__(self, other):
        """
        Проверяем идентичны ли матрицы (==)
        :param other: матрица, с которой сравниваем
        :return: True - идентичны, False - не иденичны
        """

        if type(self) != type(other):
            raise MatrixError('type mismatch', {'type1': type(self), 'type2':  type(other)})

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

        if type(self) != type(other):
            raise MatrixError('type mismatch', {'type1': type(self), 'type2':  type(other)})

        if len(self.matrix) != len(other.matrix):
            return True
        for val_our, val_other in zip(self.matrix, other.matrix):
            if val_our != val_other:
                return True

        return False

    # x > y
    def __gt__(self, other):
        pass

    # x >= y
    def __ge__(self, other):
        pass

    def __add__(self, other):
        """
        Сумма двух объектов Matrix
        :param other: матрица, с которой суммируем
        :return: результат - объект Matrix
        """
        if self.row != other.row:
            raise MatrixError('rows are not equal', {'row1': self.row, 'row2': other.row})
        if self.col != other.col:
            raise MatrixError('rows are not equal', {'col1': self.col, 'col2': other.col})

        matrix = Matrix(row=self.row, col=self.col)
        for i, (row1, row2) in enumerate(zip(self.matrix, other.matrix)):
            for j, (col1, col2) in enumerate(zip(row1, row2)):
                matrix.matrix[i][j] = col1 + col2

        return matrix

    def __sub__(self, other):
        """
        Разность двух объектов Matrix
        :param other: матрица, к которой производим разность
        :return: результат - объект Matrix
        """
        if self.row != other.row:
            raise MatrixError('rows are not equal', {'row1': self.row, 'row2': other.row})
        if self.col != other.col:
            raise MatrixError('rows are not equal', {'col1': self.col, 'col2': other.col})

        matrix = Matrix(row=self.row, col=self.col)
        for i, (row1, row2) in enumerate(zip(self.matrix, other.matrix)):
            for j, (col1, col2) in enumerate(zip(row1, row2)):
                matrix.matrix[i][j] = col1 - col2

        return matrix

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.col != other.row:
                raise MatrixError('the number of columns in the first matrix is not equal'
                                  ' to the number of rows in the second matrix',
                                  {'col_matrix1': self.col, 'row_matrix2': other.row})

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
            raise MatrixError('raw types for multiplication', {'type1': type(self), 'type': type(other)})

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
