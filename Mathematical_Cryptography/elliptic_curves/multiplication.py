from Mathematical_Cryptography.elliptic_curves import addition


def multiply(n, P, a, p):
    new_p = P
    i = 1
    while i < n:
        new_p = addition.add(new_p, P, a, p)
        i += 1
    return new_p


# print(multiply(1194, (3684, 3125), 324, 3851))
print(multiply(875, (2, 96), 171, 2671))
