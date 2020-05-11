

def find_order(g, p):
    x = 1
    _g = g
    while x < p + 1:
        if _g % p == 1:
            return x
        _g *= g
        x += 1
    return -1


