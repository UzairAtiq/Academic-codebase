n = int(input("Enter A Number : "))

#Creating a dictionary 
square = {}

#Loop from 1 to n
for i in range(1, n+1) : 
  if i % 2 == 0 : #Checking Even 
    square[i] = i*i # Assigning Key and Valye

print(square)
