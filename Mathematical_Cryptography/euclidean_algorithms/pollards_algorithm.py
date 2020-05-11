from Mathematical_Cryptography.euclidean_algorithms import compute_GCD


def use_pollards_alg(N):
    a = 2
    for j in range(2, 60):
        a = a ** j % N
        d = compute_GCD.compute_gcd(a - 1, N)[0]
        if 1 < d < N:
            return d
    return 0


N = 48356747
p = use_pollards_alg(N)
q = N//p
print("p = " + str(p) + ", q = " + str(q))
print("checking: p * q = " + str(p * q))
