from itertools import zip_longest

string1= "aaryaman"
string2 = "gupta"

result = [a + (b if b else '') for a,b in zip_longest(string1,string2,fillvalue ='')]
print(", ".join(result))
