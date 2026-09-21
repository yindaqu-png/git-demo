import itertools
import random
import functools


def combinations_std(nums, n):
    """使用标准库计算组合"""
    return list(itertools.combinations(nums, n))


class Matrix:
    def __init__(self, data=None, dim=None, init_value=0):
        if not data == None:
            for i in data:
                if len(i) != len(data[0]):
                    raise ValueError(
                        "the number of element in each row must be identical!"
                    )
            self.data = data
            self.dim = (len(data), len(data[0]))
        elif not dim == None:
            self.data = []
            for _ in range(dim[0]):
                row = [init_value] * dim[1]
                self.data.append(row)
            self.dim = dim
        else:
            raise ValueError("the matrix can't be determined!")

    def shape(self):
        return self.dim

    def reshape(self, newdim):
        if newdim[0] * newdim[1] != self.dim[0] * self.dim[1]:
            raise ValueError(
                "the size of the new matrix is not identical to the original matrix"
            )
        else:
            n1, m1 = newdim[0], newdim[1]
            self.dim = newdim
            elements = []
            for i in self.data:
                for j in i:
                    elements.append(j)
            newdata = []
            for r in range(n1):
                row = [elements[i] for i in range(m1 * r, m1 * r + m1)]
                newdata.append(row)
            self.data = newdata
            return self

    def dot(self, other):

        if self.dim[1] != other.dim[0]:
            raise ValueError("these two matrices can't multiply")
        else:
            result = Matrix(dim=(self.dim[0], other.dim[1]))
            for i in range(result.dim[0]):
                for j in range(result.dim[1]):
                    result.data[i][j] = sum(
                        [self.data[i][k] * other.data[k][j] for k in range(self.dim[1])]
                    )
            return result

    def T(self):
        m1, n1 = self.dim[0], self.dim[1]  # m1是行，n1是列
        result = Matrix(dim=(n1, m1))
        D = self.data
        data = []
        for i in range(n1):
            nr = [D[k][i] for k in range(m1)]
            data.append(nr)
        result.data = data
        return result

    def sum(self, axis=None):
        if axis == None:
            s = 0
            for i in self.data:
                for j in i:
                    s += j
            result = Matrix(data=[[s]], dim=(1, 1))
            return result
        if axis == 1:
            result = Matrix(dim=(self.dim[0], 1))
            r = []
            for i in range(self.dim[0]):
                s = sum([self.data[i][k] for k in range(self.dim[1])])
                r.append([s])
            result.data = r
        if axis == 0:
            result = Matrix(dim=(1, self.dim[1]))
            r = []
            for i in range(self.dim[1]):
                s = sum([self.data[k][i] for k in range(self.dim[0])])
                r.append(s)
            result.data = [r]

    def copy(self):
        a = []
        for x in self.data:
            a.append(x.copy())
        cop = Matrix(data=a)
        return cop

    def Kronecker_product(self, other):
        n1, m1, n2, m2 = self.dim[0], self.dim[1], other.dim[0], other.dim[1]
        result = Matrix(dim=(n1 * n2, m1 * m2))
        n3, m3 = result.dim[0], result.dim[1]
        re = []
        for i in range(n3):
            r = [
                self.data[i // n2][k] * b for k in range(m1) for b in other.data[i % n2]
            ]
            re.append(r)
        result.data = re
        return result

    def __getitem__(self, key):
        k1, k2 = key[0], key[1]
        if type(k1) == int and type(k2) == int:
            if k1 >= self.dim[0] or k2 >= self.dim[1]:
                raise ValueError("the index is out of range")
            else:
                return self.data[k1][k2]
        else:
            k1, k2 = key
            d = self.data.copy()
            r = d[k1]
            for i in range(len(r)):
                r[i] = r[i][k2]
            result = Matrix(data=r)
            return result

    def __setitem__(self, key, value):
        pass
        k1, k2 = key[0], key[1]
        if type(k1) == int and type(k2) == int:
            if k1 >= self.dim[0] or k2 >= self.dim[1]:
                raise ValueError("the index is out of range")
            else:
                self.data[k1][k2] = value
                result = Matrix(data=self.data)
                return result
        else:
            p = 0
            if k1.start == None and k1.stop == None:
                start, stop = 0, self.dim[0]
            if k1.start == None and k1.stop != None:
                start, stop = 0, k1.stop
            if k1.start != None and k1.stop == None:
                start, stop = k1.start, self.dim[0]
            else:
                start, stop = k1.start, k1.end
            for i in range(start, stop):
                self.data[i][k2] = value.data[p]
                p += 1
            result = Matrix(data=self.data)
            return result

    def __str__(self):
        rows = []
        for row in self.data:
            # 将每行的元素转换为字符串并用空格分隔
            row_str = " ".join(str(elem) for elem in row)
            rows.append(row_str)

        # 添加方括号
        result = "[[" + rows[0] + "]"
        for i in range(1, len(rows)):
            if i == len(rows) - 1:
                result += "\n [" + rows[i] + "]]"
            else:
                result += "\n [" + rows[i] + "]"

        return result

    def __pow__(self, n):
        if self.dim[0] != self.dim[1]:
            raise ValueError("these two matrices can't multiply")
        else:
            a = self.copy()
            while n > 1:
                a = a.dot(self)
                n -= 1
            return a

    def __add__(self, other):
        if self.dim[1] != other.dim[1] or self.dim[0] != other.dim[0]:
            raise ValueError("these two matrices can't multiply")
        else:
            a, b = self.dim  # a行数 b列数
            data = []
            for x in range(a):
                c = []
                for t in range(b):
                    c1 = self[x, t] + other[x, t]
                    c.append(c1)
                data.append(c)
            t = Matrix(data=data)
            return t

    def __sub__(self, other):
        if self.dim[1] != other.dim[1] or self.dim[0] != other.dim[0]:
            raise ValueError("these two matrices can't mutiply")
        else:
            a, b = self.dim  # a行数 b列数
            data = []
            for x in range(a):
                c = []
                for t in range(b):
                    c1 = self[x, t] - other[x, t]
                    c.append(c1)
                data.append(c)
            t = Matrix(data=data)
            return t

    def __mul__(self, other):
        if self.dim[1] != other.dim[1] or self.dim[0] != other.dim[0]:
            raise ValueError("these two matrices can't multiply")
        else:
            a, b = self.dim  # a行数 b列数
            data = []
            for x in range(a):
                c = []
                for t in range(b):
                    c1 = self[x, t] * other[x, t]
                    c.append(c1)
                data.append(c)
            t = Matrix(data=data)
            return t

    def __len__(self):
        a, b = self.dim
        c = a * b
        return c

    # str函数已经在前面实现
    def det(self):
        if self.dim[0] != self.dim[1]:
            raise ValueError("只有方阵才有行列式")

        n = self.dim[0]

        # 创建副本以避免修改原矩阵
        mat = self.copy()
        det = 1

        for i in range(n):
            # 找到主元
            pivot = i
            while (
                pivot < n and mat.data[pivot][i] == 0
            ):  # i行i列，即主元所在位置，要判断其是否为0，
                pivot += 1

            if pivot == n:
                return 0  # 行列式为0

            if pivot != i:
                # 交换行
                mat.data[i], mat.data[pivot] = mat.data[pivot], mat.data[i]
                det *= -1  # 行交换改变符号

            # 消元
            pivot_value = mat.data[i][i]
            det *= pivot_value

            for j in range(i + 1, n):
                if mat.data[j][i] != 0:  # 对主元所在列逐行处理
                    factor = mat.data[j][i] / pivot_value
                    for k in range(i, n):
                        mat.data[j][k] -= (
                            factor * mat.data[i][k]
                        )  # 保证主元所在列往后延都是0

        return det

    def bianhuan1(self, a, n):
        for x in range(len(self.data[a])):
            self.data[a][x] /= n
        return self

    def bianhuan2(self, a, b):
        self.data[a], self.data[b] = self.data[b], self.data[a]
        return self

    def bianhuan3(self, a, b, n):
        for x in range(len(self.data[a])):
            self.data[a][x] -= self.data[b][x] * n
        return self

    def inverse(self):
        n, b = self.dim
        print(self)
        if n != b:
            raise ValueError("不是方阵")
        if self.det() == 0:
            raise ValueError("无逆矩阵")
        else:
            data1 = []

            for i in range(n):
                a = [0] * n
                a[i] = 1
                data1.append(a)
            mat1 = Matrix(data=data1)
            mat = self.copy()
            for i in range(n):
                # 找到主元
                pivot = i
                while (
                    pivot < n and mat.data[pivot][i] == 0
                ):  # i行i列，即主元所在位置，要判断其是否为0，
                    pivot += 1

                if pivot != i:
                    # 交换行
                    mat.data[i], mat.data[pivot] = mat.data[pivot], mat.data[i]
                    mat1.data[i], mat1.data[pivot] = mat1.data[pivot], mat1.data[i]
            data2 = []
            for x in range(n):
                t = mat.data[x] + mat1.data[x]
                data2.append(t)
            mat2 = Matrix(data=data2)

            for i in range(n):
                a1 = mat2.data[i][i]
                mat2.bianhuan1(i, a1)

                for x in range(i + 1, n):
                    a2 = mat2.data[x][i]
                    mat2.bianhuan3(x, i, a2)
            for i in range(n - 1, -1, -1):
                for j in range(i - 1, -1, -1):
                    b1 = mat2.data[j][i]
                    mat2.bianhuan3(j, i, b1)
            return mat2[:, n:]

    def son(self, n):

        rows, cols = self.dim

        # 存储所有子矩阵的列表
        all_submatrices = []

        # 生成所有可能的行索引组合
        row_combinations = list(itertools.combinations(range(rows), n))
        # 生成所有可能的列索引组合
        col_combinations = list(itertools.combinations(range(cols), n))

        # 遍历所有行组合和列组合
        # 生成两个排列，这样在for循环的时候就有两个生成器可以用
        # 之前的问题是，只有一种排列，共用了一个生成库
        for row_indices in row_combinations:
            for col_indices in col_combinations:
                # 提取子矩阵数据
                submatrix_data = []
                for row_idx in row_indices:
                    row = []
                    for col_idx in col_indices:
                        row.append(self.data[row_idx][col_idx])
                    submatrix_data.append(row)

                # 创建子矩阵对象并添加到列表
                submatrix = Matrix(data=submatrix_data)
                all_submatrices.append(submatrix)

        return all_submatrices

    def rank(self):
        mat = self.copy()
        a, b = mat.dim
        n = min(a, b)
        for x in range(n, -1, -1):
            for t in mat.son(x):
                a1 = t.det()
                if a1 != 0:
                    return x


def I(n):
    data1 = []

    for i in range(n):
        a = [0] * n
        a[i] = 1
        data1.append(a)
    mat1 = Matrix(data=data1)
    return mat1


# 最后十个


def narray(dim, init_value=1):
    return Matrix(dim=dim, init_value=init_value)


def arange(start, end, step):
    elements = list(range(start, end, step))
    return Matrix(data=[elements])


def zeros(dim):
    return Matrix(dim=dim, init_value=0)


def zeros_like(matrix):
    return Matrix(dim=matrix.shape(), init_value=0)


def ones(dim):
    return Matrix(dim=dim, init_value=1)


def ones_like(matrix):
    return Matrix(dim=matrix.shape(), init_value=1)


def nrandom(dim):
    result = Matrix(dim=dim)
    for i in range(dim[0]):
        for j in range(dim[1]):
            result.data[i][j] = random.random()
    return result


def nrandom_like(matrix):
    dim = matrix.shape()
    return nrandom(dim)


def concatenate(items, axis=0):
    items = list(items)
    if not all(isinstance(item, Matrix) for item in items):
        raise TypeError("all items must be Matrix instances")

    if axis == 0:
        n = items[0].shape()[1]
        if not all(item.shape()[1] == n for item in items):
            raise ValueError(
                "all matrices must have the same number of columns for axis=0"
            )

        all_rows = []
        for item in items:
            all_rows.extend(item.data)

        return Matrix(data=all_rows)

    else:
        m = items[0].shape()[0]
        if not all(item.shape()[0] == m for item in items):
            raise ValueError(
                "all matrices must have the same number of rows for axis=1"
            )

        result_data = []
        for i in range(m):
            new_row = []
            for item in items:
                new_row.extend(item.data[i])
            result_data.append(new_row)

        return Matrix(data=result_data)


def vectorize(func):
    def vectorized_func(matrix):
        result = Matrix(dim=matrix.shape())
        m, n = matrix.shape()
        for i in range(m):
            for j in range(n):
                result.data[i][j] = func(matrix.data[i][j])

        return result

    vectorized_func.__name__ = func.__name__
    vectorized_func.__doc__ = func.__doc__

    return vectorized_func


if __name__ == "__main__":
    print("test here")
    pass
