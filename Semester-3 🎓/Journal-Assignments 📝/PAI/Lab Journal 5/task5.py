a = 30
b = 40
c = 60

def checkLargest(x,y,z) : 
  if x > y and x > z :
    print(x)
  elif y > x and y > z :
    print(y)
  elif z > x and z > y :
    print(z)
  else :
    print("All Numbers are equal")

print("The Largest Number is : ")
checkLargest(a,b,c)
