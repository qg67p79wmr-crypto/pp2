x = lambda a, b : a * b
print(x(5, 6))

#2
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11))

#