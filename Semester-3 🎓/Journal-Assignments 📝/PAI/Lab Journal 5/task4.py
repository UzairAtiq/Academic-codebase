word = input("Enter a word or Check if it is a Palindrome: ")

def checkPalindrome(word) :
  wordList = [] 
  wordList = list(word)
  revWordList = wordList[::-1]
  if  wordList == revWordList : 
    print("The word is a palindrome")
  else : 
    print("The word is not a palindrome")
  
checkPalindrome(word)
