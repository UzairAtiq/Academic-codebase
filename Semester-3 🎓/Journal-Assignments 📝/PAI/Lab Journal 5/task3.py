n = int(input("Enter a number to calculate its factorial: "))

#Function to calculate the factorial
def calFactorial(n) :
  #Variable for factorial
  factorial = 1 
  #List to store the Numbers for factorial
  numbers = []
  for i in range(1, n+1) :
    numbers.append(i)
  for x in numbers : 
    factorial *= x
  print(numbers)
  return factorial
print(calFactorial(n))