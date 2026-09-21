# Test code for IEEE course final project
# Fan Cheng, 2024

import minimatrix as mm
import random

matrix_mat = mm.Matrix(data=[[1, 2, 3], [6, 5, 4], [7, 8, 9]])
print(matrix_mat)

m24 = mm.arange(0, 24, 1)
print(m24.reshape([3, 8]))
print(m24.reshape([24, 1]))
print(m24.reshape([4, 6]))

m0 = mm.zeros((3, 3))
print(m0)
mm.zeros_like(m24)

m1 = mm.ones((3, 3))
print(m1)
mm.ones_like(m24)

mr = mm.nrandom((3, 3))
print(mr)
mm.nrandom_like(m24)


x = mm.nrandom((1000, 100))
w = mm.nrandom((100, 1))
e = mm.nrandom((1000, 1))
# 假设 nrandom 返回 [0,1) 的随机数，减去0.5得到零均值噪声
e = e - mm.Matrix(dim=(1000, 1), init_value=0.5)  # 或者使用其他方式

y = x.dot(w) + e

# 计算最小二乘估计
nw = x.T().dot(x).inverse().dot(x.T()).dot(y)

# 简单比较
print("前100个参数对比:")
print("真实 w\t\t估计 w_hat\t\t差值")
for i in range(100):
    w_val = w[i, 0]
    nw_val = nw[i, 0]
    diff = nw_val - w_val
    print(f"{w_val:.6f}\t{nw_val:.6f}\t{diff:.6f}")

# 计算平均误差
total_error = 0
for i in range(100):
    w_val = w[i, 0]
    nw_val = nw[i, 0]
    total_error += abs(nw_val - w_val)

avg_error = total_error / 100
print(f"\n平均绝对误差: {avg_error:.6f}")
