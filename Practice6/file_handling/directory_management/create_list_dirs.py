import os
for (root,dirs,files) in os.walk('C:/W3school/',topdown=True):
  print("Directory path: %s"%root)
  print("Directory Names: %s"%dirs)
  print("Files Names: %s"%files)