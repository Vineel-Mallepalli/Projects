from Mathematical_Cryptography.discrete_logs_and_groups.find_sqrt_mod import find_sqrt_mod
from Mathematical_Cryptography.elliptic_curves import addition
import numpy


# for an equation Y^2 = X^3 + AX + B in E(F_p), we find possible x,y pairings.
def find_possible_xy(a, b, p):
    pairings = []
    f = lambda x: (x ** 3 + a * x + b) % p
    for i in range(p):
        y_sq = find_sqrt_mod(f(i), p)
        for j in y_sq:
            pairings.append((i, j))
    return pairings


def create_addition_table(points, a, p):
    nums = [(-1, -1)] + points
    n = len(nums)
    matrix = numpy.zeros((n, n), dtype=(int, 2))
    matrix[0] = numpy.array(nums, dtype=(int, 2))
    for row in range(n):
        matrix[row][0] = nums[row]
    for i in range(1, n):
        for j in range(1, n):
            matrix[i][j] = addition.add(tuple(matrix[i][0]), tuple(matrix[0][j]), a, p)
    return matrix


# print(find_possible_xy(1, 2, 5))
# print(find_possible_xy(2, 3, 7))
print(create_addition_table(find_possible_xy(2, 5, 11), 2, 11))
