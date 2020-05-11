
def solve_subset_sum(m, s):
    x = [0 for num in m]
    for i in range(len(m) - 1, -1, -1):
        if s >= m[i]:
            x[i] = 1
            s -= m[i]
        else:
            x[i] = 0
    return x


arr = [5, 14, 30, 75, 160, 351, 750, 1579, 3253, 6500]
print(solve_subset_sum(arr, 4528))
