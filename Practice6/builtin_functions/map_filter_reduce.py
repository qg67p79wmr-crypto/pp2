from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

mapped = list(map(lambda x: x * 2, numbers))
print("map:", mapped)

filtered = list(filter(lambda x: x % 2 == 0, numbers))
print("filter:", filtered)

result = reduce(lambda x, y: x + y, numbers)
print("reduce:", result)