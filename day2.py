# product id ranges
# find sum of all ids in the ranges that are of the form X repeated twice, e.g. 11, 6464, 123123

def is_invalid_id(n: int) -> bool:
    s = str(n)
    for pattern_len in range(1, len(s) // 2 + 1):
        if len(s) % pattern_len == 0:
            pattern = s[:pattern_len]
            repetitions = len(s) // pattern_len
            if s == pattern * repetitions and repetitions >= 2:
                return True
    return False


sol = 0

with open("input2") as f:
    data = f.readlines()
    for line in data:
        line = line.strip()
        if not line:
            continue

        parts = line.split(",")
        for part in parts:
            part = part.strip()
            if not part:
                continue

            start_str, end_str = part.split("-")
            start, end = int(start_str), int(end_str)

            # brute force over the entire range
            for n in range(start, end + 1):
                if is_invalid_id(n):
                    sol += n

print(sol)
