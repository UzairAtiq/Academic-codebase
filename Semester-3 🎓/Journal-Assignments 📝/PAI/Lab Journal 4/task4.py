dict1 = {
  "x" : 20,
  "y" : 30,
  "z" : 40
}

dict2 = {
  "x" : 10,
  "y" : 40,
  "z" : 20
}

dict3 = {}

#Main Logic for checking and assigning the larger value 
for key in dict1 : 
  if dict1[key] > dict2[key] :
    dict3[key] = dict1[key]
  else : 
    dict3[key] = dict2[key]

print(dict3)
