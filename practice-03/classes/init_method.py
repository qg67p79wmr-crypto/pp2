class Person:
    def __init__(self, name,age = 18):
        self.name = name
        self.age = age

p1 = Person("Emil")
p2 = Person("Tobias", 25)
print(p1.name, p1.age)
print(p2.age)
#challenges
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(self.name + " says Woof!")


d1 = Dog("Buddy", 3)
d1.bark()

class Car:
    def __init__(self, brand):
        self.brand = brand

    def show(self):
        print(self.brand)

c1 = Car("Ford")
c1.show()
