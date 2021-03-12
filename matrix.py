# Наши модули
from Error import *


class Matrix(object):

    def __init__(self, matrix=None, row=None, col=None):
        """
        Инициализирует матрицу, переданную вида [[], [], ..., []]
        или
        Инициализирует нулевую матрицу размера row x col
        :param matrix: матрица вида [[1,2,3], [2, 0]]
        :param row: количество строк
        :param col: количество столбцов
        """

        # сделать try-except для разных переданных значений и выдавание своих ошибок в случае с этим !!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if not matrix is None:
            # Создаем матрицу вида matrix. Пример:
            # Дана матрица:
            # [ [1, 2, 3, 4],
            #   [5, 6],
            #   [7],
            #   [8, 9] ]
            # Будет создана матрица:
            # [ [1, 2, 3, 4],
            #   [5, 6, 0, 0],
            #   [7, 0, 0, 0],
            #   [8, 9, 0, 0] ]
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
                        self.matrix[i_row].append(matrix[i_row][col])
                    except IndexError:
                        self.matrix[i_row].append(0)

            self.row = rows
            self.col = cols
        elif not (row is None and col is None):
            # Создаем нулевую матрицу матрицу
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
