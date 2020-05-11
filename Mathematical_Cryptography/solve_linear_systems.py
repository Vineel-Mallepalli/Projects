import numpy as np


def solve_linear_eqs(lhs_vals, rhs_vals):
    a = np.array(lhs_vals)
    b = np.array(rhs_vals)
    x = np.linalg.solve(a, b)
    return x


# print(solve_linear_eqs([[25453, -16096], [9091, -5749]], [155340, 55483]))
# print(solve_linear_eqs([[4, -57], [13, -45]], [155340, 55483]))
# v1 = [58, -110, -10]
# v2 = [53, -112, -119]
# v3 = [-68, 35, 123]
e = [8930810, -44681748, 75192665]
# t = solve_linear_eqs([v1, v2, v3], e)
# print(t)
# v = [8930820, -44681745, 75192657]
w1 = [324850, 165782, 485054]
w2 = [-1625176, -829409, -2426708]
w3 = [2734951, 1395775, 4083804]
print(solve_linear_eqs([w1, w2, w3], e))
# new_t = solve_linear_eqs([w1, w2, w3], v)
# print(new_t)


