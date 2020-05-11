from Mathematical_Cryptography.euclidean_algorithms import compute_GCD


def compute_lcm(a, b):
    gcd = compute_GCD.compute_gcd(a, b)[0]
    return a * b // gcd


# print(compute_lcm(5, 6))
