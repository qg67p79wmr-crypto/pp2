from functools import reduce

numbers = [10, 15, 20, 25, 30]

# map() - add 5 to each number
new_numbers = list(map(lambda x: x + 5, numbers))
print("map:", new_numbers)

# filter() - keep numbers greater than 20
big_numbers = list(filter(lambda x: x > 20, numbers))
print("filter:", big_numbers)

# reduce() - sum all numbers
total = reduce(lambda x, y: x + y, numbers)
print("reduce:", total)