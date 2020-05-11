from randomTestpkg import solve_quadratic
from Mathematical_Cryptography.euclidean_algorithms import fast_powers


def compute_gcd(a, b):
    if a < 0 or b < 0:
        return None
    elif a == 0 or b == 0:
        return (b, 0, 1) if a == 0 else (a, 1, 0)
    elif a == b:
        return a, 1, 0
    else:
        init_gcd = compute_gcd_helper(a, b, a, b) if (a > b) else swap(compute_gcd_helper(b, a, b, a))
        g, u, v = init_gcd
        while u < 0:
            u += b // g
            v -= a // g
        return g, u, v


def compute_gcd_helper(a, b, g, y, u=1, x=0):
    if y == 0:
        v = (g - a * u) // b
        return g, u, v
    q = g // y
    t = g - q * y  # 0 <= t < y
    s = u - q * x
    u, g = x, y
    x, y = s, t
    return compute_gcd_helper(a, b, g, y, u, x)


def swap(tup):
    if len(tup) == 3:
        return tup[0], tup[2], tup[1]
    return None


def has_inverse(a, p):
    if compute_gcd(a, p)[0] == 1:
        return True
    return False


def compute_inverse(a, p):
    if not has_inverse(a, p):
        return -1
    b = 1
    while b < p:
        if (a * b) % p == 1:
            return b
        b += 1
    return -1


# print(compute_gcd(5, 0))
# print(compute_gcd(12849217045006222, 6485880443666222))
# print(compute_inverse(3, 11))
# print(compute_inverse(4, 7))
print(compute_inverse(4392, 8387))
print((2683 * 26560) % 8387)


