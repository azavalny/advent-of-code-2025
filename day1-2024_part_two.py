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

    similarity_score=0
    for leftnum in left:
        num_appearances = 0
        for rightnum in right:
            if leftnum == rightnum:
                num_appearances += 1
        similarity_score += leftnum * num_appearances
    print(similarity_score)