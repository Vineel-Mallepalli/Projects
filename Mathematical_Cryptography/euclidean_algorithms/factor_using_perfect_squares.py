import math
from Mathematical_Cryptography.euclidean_algorithms import compute_GCD


def factor(N, k, b_init):
    b = b_init
    while b < N:
        val = k * N + b ** 2
        sqrt = math.sqrt(val)
        if sqrt.is_integer():
            return compute_GCD.compute_gcd(N, int(sqrt) + b)[0], compute_GCD.compute_gcd(N, int(sqrt) - b)[0]
        b += 1
    return 0


print(factor(143041, 247, 1))
print(313 * 457 == 143041)
print(factor(1226987, 3, 36))
print(653 * 1879 == 1226987)
print(factor(2510839, 21, 90))
print(1051 * 2389 == 2510839)
