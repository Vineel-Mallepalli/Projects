from Mathematical_Cryptography.euclidean_algorithms.compute_GCD import compute_inverse
from Mathematical_Cryptography.discrete_logs_and_groups import find_sqrt_mod


# representing origin as (-1, -1)
def add(p1, p2, a, p):
    if p1 == (-1, -1):
        return p2
    if p2 == (-1, -1):
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and y1 == -y2 % p:
        return -1, -1
    if p1 == p2:
        lamb = (3 * (x1 ** 2) + a) * compute_inverse(2.0 * y1, p)
    else:
        lamb = ((y2 - y1) * compute_inverse((x2 - x1) % p, p)) % p
    x3 = lamb ** 2 - x1 - x2
    y3 = lamb * (x1 - x3) - y1
    return x3 % p, y3 % p


def f(x, a, b): return x ** 3 + a * x + b


# print(find_sqrt_mod.find_sqrt_mod(f(2, 171, 853) % 2671, 2671))
# print(add((4, 0), (1, 2), 1, 5))
# print(add((4, 0), (1, 3), 1, 5))
# print(add((4, 0), (4, 0), 1, 5))
# print(add((1, 2), (1, 2), 1, 5))

