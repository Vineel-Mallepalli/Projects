def prime_factorize(n):
    if is_prime(n):
        return [n]
    a = 2
    ans = []
    while n > 1:
        if n % a == 0:
            ans.append(a)
            n //= a
        else:
            a = 3 if a == 2 else a + 2
    return ans


def is_prime(n):
    # Corner cases
    if n <= 1:
        return False
    if n <= 3:
        return True

    # This is checked so that we can skip
    # middle five numbers in below loop
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i = i + 6

    return True


print(prime_factorize(384))
# print(prime_factorize(5))
# print(prime_factorize(25))
# print(prime_factorize(6916))
# print(prime_factorize(6000))
# print(prime_factorize(174385766))

