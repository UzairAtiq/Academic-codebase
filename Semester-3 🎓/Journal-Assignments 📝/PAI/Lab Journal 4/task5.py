newdict = {}

n = int(input("How Many Students Details You want to Enter :"))

#Taking input for the dictionary
for i in range(n) : 
  key = input("Enter the Name of Student: ")
  value = int(input("Enter Marks of the Student: "))
  newdict[key] = value

valueToSearch = int(input("Enter Value You want to search:"))

#Searcing the value and printing the key if found
for key ,values in newdict.items() : 
  if valueToSearch == values : 
   print(key)
