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


# print(compute_gcd(5, 0))
# print(compute_gcd(527, 1258))
# print(compute_gcd(228, 1056))
# print(compute_gcd(163961, 167181))
# print(compute_gcd(3892394, 239847))
# print(compute_gcd(12849217045006222, 6485880443666222))
print(12849217045006222 // 87192883)
print(6485880443666222 // 87192883)


