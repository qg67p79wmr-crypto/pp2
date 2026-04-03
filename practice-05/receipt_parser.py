import re

#Check if the string starts with "The" and ends with "Spain":

txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)

if x:
  print("YES! We have a match!")
else:
  print("No match")

 ##################################2
import re
txt = "The rain in Spain"
n= re.findall("Portugal", txt)
print(n)
if (x):
  print("Yes, there is at least one match!")
else:
  print("No match")


########
import re

txt = "The rain in Spain"
x = re.search("\s", txt)

print("The first white-space character is located in position:", x.start()) 
# output: The first white-space character is located in position: 3
#If no matches are found, the value None is returned




import re

#Split the string at every white-space character:

txt = "The rain in Spain"
x = re.split("\s", txt)
print(x)
##['The', 'rain', 'in', 'Spain']





import re

#Split the string at the first white-space character:

txt = "The rain in Spain"
x = re.split("\s", txt, 1)
print(x)

###output:['The', 'rain in Spain']

import re ##. SUB 
txt = "The rain in Spain"
x = re.sub("\s", "9", txt,1)
print(x) # output: The9rain in Spain