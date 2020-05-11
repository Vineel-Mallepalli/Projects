import random
import math
from Mathematical_Cryptography.elliptic_curves import multiplication
from Mathematical_Cryptography.elliptic_curves import addition


def solve_ecdlp(P, Q, a, p):
    list_len = 3 * int(math.sqrt(p))
    j_vals = []
    k_vals = []
    j_p_vals = []
    k_pplusq_vals = []
    for i in range(list_len):
        j = 0
        k = 0
        while j <= 0 or j in j_vals or j in k_vals:
            j = random.randint(1, p - 1)
        while k <= 0 or k in k_vals or k in j_vals:
            k = random.randint(1, p - 1)
        j_vals.append(j)
        k_vals.append(k)
        j_p = multiplication.multiply(j, P, a, p)
        k_pplusq = addition.add(multiplication.multiply(k, P, a, p), Q, a, p)
        if j_p in k_pplusq_vals:
            j_u = j
            k_v = k_vals[k_pplusq_vals.index(j_p)]
            return j_u - k_v
        if k_pplusq in j_p_vals:
            j_u = j_vals[j_p_vals.index(k_pplusq)]
            k_v = k
            return j_u - k_v
        j_p_vals.append(j_p)
        k_pplusq_vals.append(k_pplusq)
    return None


# print(solve_ecdlp((1980, 431), (2110, 543), 171, 2671))
