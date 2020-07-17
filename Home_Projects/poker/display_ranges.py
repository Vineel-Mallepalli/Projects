

# display a colored board of given ranges
# ranges are given in the following format: [[premiums/raises], [calls]]
def display_range(range):
    if len(range) != 2:
        return
