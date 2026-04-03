names = ["Ali", "Dana", "Aruzhan"]
scores = [90, 85, 95]

for index, name in enumerate(names, start=1):
    print(index, name)

for name, score in zip(names, scores):
    print(name, score)