

def double_and_add(p, n):
    q = p
    r = (0, 1, 0)
    while n > 0:
        if n % 2 == 1:
            r = r + q
        q = 2 * q
        n = n // 2
    return r
