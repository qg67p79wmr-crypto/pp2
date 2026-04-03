import os
os.remove("demofile.txt")

import os
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist")


import os
os.rmdir("myfolder") 


import shutil
import os

shutil.copy("sample.txt", "sample_backup.txt")
print("File copied")

if os.path.exists("sample_backup.txt"):
    print("Backup exists")

if os.path.exists("sample_backup.txt"):
    os.remove("sample_backup.txt")
    print("Backup deleted safely")
else:
    print("File not found")