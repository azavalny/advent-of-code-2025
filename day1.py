with open("input1") as f:
    sol = 0
    rotations = f.readlines()
    start = 50

    for rotation in rotations:
        direction = rotation[0]
        amount = int(rotation[1:])

        if direction == "R":
            sol += (start + amount) // 100 - start // 100
            start = (start + amount) % 100
        else:
            start_reflected = (100 - start) % 100 # so we can use the same logic from right
            sol += (start_reflected + amount) // 100 - start_reflected // 100
            start = (start - amount) % 100

    print(sol)
