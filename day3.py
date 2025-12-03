def best_k_digits_in_order(digits, k):
    stack = []
    remove = len(digits) - k  # how many digits we can drop

    for d in digits:
        while stack and remove > 0 and stack[-1] < d:
            stack.pop()
            remove -= 1
        stack.append(d)

    # truncate if stack is longer than k
    return stack[:k]


with open("input3") as f:
    banks = f.readlines()

total = 0

for bank in banks:
    digits = [int(x) for x in bank.strip()]
    best12 = best_k_digits_in_order(digits, 12)

    val = int("".join(map(str, best12)))

    total += val

print(total)