import os
import shutil

os.makedirs("source", exist_ok=True)
os.makedirs("destination", exist_ok=True)

with open("source/test.txt", "w", encoding="utf-8") as file:
    file.write("Hello from source")

shutil.copy("source/test.txt", "destination/test_copy.txt")
print("File copied")

shutil.move("source/test.txt", "destination/test_moved.txt")
print("File moved")