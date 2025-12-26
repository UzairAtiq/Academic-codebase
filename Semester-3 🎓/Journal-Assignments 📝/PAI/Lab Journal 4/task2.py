sentence = input("Enter Your Sentence: ")
#Splitting into a list of words
s = sentence.split()

dictnew = {}

#Main Logic to check frequency using the get method
for word in s : 
 dictnew[word] = dictnew.get(word,0) +1

print(dictnew)
