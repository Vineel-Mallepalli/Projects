

def find_sqrt_mod(a, p):
    ans = []
    for i in range(p):
        if (i * i) % p == a:
            ans.append(i)
    return ans
