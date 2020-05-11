from Mathematical_Cryptography.discrete_logs_and_groups import order
from Mathematical_Cryptography.euclidean_algorithms import compute_GCD
import math


def shanks_algorithm(g, h, p):
    big_n = order.find_order(g, p)
    small_n = 1 + math.floor(math.sqrt(big_n))
    baby_steps = []
    giant_steps = []
    u = (compute_GCD.compute_inverse(g, p) ** small_n) % p
    for i in range(small_n + 1):
        baby_steps.append(g ** i % p)
        giant_steps.append(h * u ** i % p)
    for i in range(len(baby_steps)):
        for j in range(len(giant_steps)):
            if baby_steps[i] == giant_steps[j]:
                return i + j * small_n
    return -1


print(shanks_algorithm(11, 21, 71))
print(shanks_algorithm(156, 116, 593))
print(shanks_algorithm(650, 2213, 3571))
