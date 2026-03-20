with open("sample.txt", "w", encoding="utf-8") as file:
    file.write("Hello\n")
    file.write("My name is Darina\n")
    file.write("I study Python\n")

print("File created and data written")


#append
with open("sample.txt", "a", encoding="utf-8") as file:
    file.write("This is a new line\n")
    file.write("Python is easy\n")

with open("sample.txt", "r", encoding="utf-8") as file:
    print(file.read())