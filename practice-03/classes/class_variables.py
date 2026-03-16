class Student:
    university = "KBTU"

    def __init__(self, name):
        self.name = name

s1 = Student("Katya")
s2 = Student("Darina")

print(s1.name)
print(s2.name)
print(s1.university)
print(s2.university)