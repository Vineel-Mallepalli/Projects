import math


def fast_power_mod(base, power, mod=1000000007):
    """
    Returns the result of a^b i.e. a**b
    We assume that a >= 1 and b >= 0

    Remember two things!
     - Divide power by 2 and multiply base to itself (if the power is even)
     - Decrement power by 1 to make it even and then follow the first step
    """

    result = 1
    while power > 0:
        # If power is odd
        if power % 2 == 1:
            result = (result * base) % mod

        # Divide the power by 2
        power = power // 2
        # Multiply base to itself
        base = (base * base) % mod

    return result


def fast_power_exact(base, power):
    """
    Returns the result of a^b i.e. a**b
    We assume that a >= 1 and b >= 0

    Remember two things!
     - Divide power by 2 and multiply base to itself (if the power is even)
     - Decrement power by 1 to make it even and then follow the first step
    """

    result = 1
    while power > 0:
        # If power is odd
        if power % 2 == 1:
            result = (result * base)

        # Divide the power by 2
        power = power // 2
        # Multiply base to itself
        base = (base * base)

    return result


# print(fast_power_mod(2, 4, 15))
# print(fast_power_mod(21, 36, 37))
# print(fast_power_mod(892383, 103, 2038667))
# print(fast_power_mod(317730, 810367, 2038667))
# print("")
# print(fast_power_exact(2, 4))  # Output: 16
# print(fast_power_exact(3, 4))  # Output: 81
# print(fast_power_exact(2, 100))  # Output: 976371285
