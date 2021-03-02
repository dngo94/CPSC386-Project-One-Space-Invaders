from vector import Vector
from copy import deepcopy

class Matrix:
    def __init__(self, rows, cols, *li):
        self.cols = cols
        self.rows = rows
        self.columns = []
        for i in range(cols):
            self.columns.append(Vector(*li[i * rows : (i+1) * rows]))

    def __str__(self):
        s = '\nMatrix... [\n'
        for col in range(self.cols):
            s += '   [  '
            for row in range(self.rows):
                val = self.columns[col].idx(row)
                if abs(val) < 1e-6: val = 0.0
                s += f'{val:2.0f}  '
            s += ']\n'
        return s + ']'

    def __add__(self, o):        # operator+
        mat = deepcopy(self)
        if isinstance(o, float):
            for i in range(self.cols):
                mat.columns[i] += o
        else:
            self.check_dims(self, o)
            for i in range(self.cols):
                mat.columns[i] += o.columns[i]
        return mat

    def __mul__(self, o):        # operator*
        mat = deepcopy(self)
        if isinstance(o, float):
            for i in range(self.cols):
                mat.columns[i] += o
        self.check_dims(self, o)

    def __rmul__(self, o):
        self.check_dims(self, o)

    def __truediv__(self, o:float): return 1.0/o * self

    def __neg__(self):         # operator-
        mat = copy(self)
        for i in range(len(self.cols)):
            mat.columns[i] *= -1
        return mat

    def __ne__(self, v): return not self == v    #operator!=

    def __eq__(self, v):
        if self.cols != v.cols: return False
        for i in range(self.cols):
            if self.columns[i] != v.columns[i]: return False
        return True

    def transpose(self):
        mat = deepcopy(self)             # make a real copy, don't just alias the original using copy
        for c in range(self.cols):
            for r in range(self.rows):
                mat.columns[c].setidx(r, self.columns[r].idx(c))
        return mat

    def rc(self, row, col): return self.columns[col].idx(row)

    def determinant(self):
        self.check_square()
        rc = self.rc
        if self.rows == 1: return rc(0, 0)
        elif self.rows == 2: return rc(0,0)*rc(1,1) - rc(1,0)*rc(0,1)
        elif self.rows == 3: return   rc(0,0)*(rc(1,1)*rc(2,2) - rc(1,2)*rc(2,1)) \
                                    - rc(0,1)*(rc(1,0)*rc(2,2) - rc(1,2)*rc(2,0)) \
                                    + rc(0,2)*(rc(1,0)*rc(2,1) - rc(1,1)*rc(2,0))
        else: raise NotImplementedError('determinants for 4x4 matrices and above not yet implemented')

    def minors(self): raise NotImplementedError('minors not implemented yet')

    def covariant(self): raise NotImplementedError('covariant not implemented yet')

    def adjugate(self): return self.covariant().transpose()

    def inverse(self): raise NotImplementedError('inverse not implemented yet')

    def check_square(self):
        if self.rows != self.cols: raise ValueError('not a square matrix')

    @classmethod
    def identity(cls, dims):
        values = []
        for r in range(dims):
            for c in range(dims):
                values.append(1 if r == c else 0)
        return Matrix(dims, dims, *values)

    @staticmethod
    def rotate(li, n): return li[n:] + li[:n]

    @staticmethod
    def check_dims(a, b):
        if a.rows != b.rows or a.cols != b.cols: raise ValueError('dimensions do not match')


    @staticmethod
    def run_tests():
        mat = Matrix(1, 1, 5)
        print(f'mat is: {mat}')

        mat2x2 = Matrix(2, 2, 1, 2, 3, 4)
        print(f'mat2x2 is: {mat2x2}')
        print(f'mat2x2.det() is: {mat2x2.determinant()}')

        mat2x2T = mat2x2.transpose()
        print(f'mat2x2T = {mat2x2T}')
        print(f'mat2x2T.det() is: {mat2x2T.determinant()}')

        sum2x2 = mat2x2 + mat2x2T
        print(f'sum2x2 is {sum2x2}')

        mat3x3 = Matrix(3, 3, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        print(f'mat3x3 is: {mat3x3}')
        print(f'mat3x3.det() is: {mat2x2.determinant()}')

        mat3x3T = mat3x3.transpose()
        print(f'mat3x3T = {mat3x3T}')
        print(f'mat3x3T.det() is: {mat3x3T.determinant()}')

        sum3x3 = mat3x3 + mat3x3T
        print(f'sum2x2 is {sum3x3}')

        for i in range(6):
            print(f'identity{i}x{i} is: {Matrix.identity(i)}')

        # sum3x3.inverse()