def my_function(x, y):
   return x + y

result = my_function(5, 3)
print(result)

#2
def my_function():
   return (10, 20)

x, y = my_function()
print("x:", x)
print("y:", y)

#3

def my_function(*, name):
   print("Hello", name)

my_function(name = "Emil")