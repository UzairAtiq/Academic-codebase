digits = int(input("Enter a number to Sum its digits:"))
digit = [] # List to store individual digits

#variable to store the total sum
total = 0

#Function to calculate the sum
def sumOfDigits(n) :
  for d in str(n) : 
    digit.append(int(d))
  total = sum(digit)
  return total 

totalSum = sumOfDigits(digits)

print(totalSum)
