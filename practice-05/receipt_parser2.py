import re

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.span()) #(12, 17)

import re

#The string property returns the search string:

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.string) #The rain in Spain

import re

#Search for an upper case "S" character in the beginning of a word, and print the word:

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.group()) #Spain


import re
txt = 'The rain in Spain'
x = re.findall('[a-c]', txt)
print(x)