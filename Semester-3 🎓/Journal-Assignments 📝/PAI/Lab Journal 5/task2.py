n = int(input("Enter To check if the numeber is prime: "))

#Function to check if a number is prime
def isPrime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

print(isPrime(n))
