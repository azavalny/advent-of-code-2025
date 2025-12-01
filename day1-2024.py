# chief historian 1 of first 50 places
# mark place checked with stars

# location ids
# pair smallest number in left with smallest number in right
# within each pair, figure out how far apart the two numbers are
# solution is sum of all those distances

with open("day1-2024_input.txt") as f:
    data = f.readlines()
    left = [int(x.rstrip("\n").split(" ")[0]) for x in data]
    right = [int(x.rstrip("\n").split(" ")[-1]) for x in data]

    left.sort()
    right.sort()
    total_distance = 0
    for l, r in zip(left, right):
        total_distance += abs(l - r)
    print(total_distance)