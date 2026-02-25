import tkinter as tk

root = tk.Tk()
root.title("Main Window")
root.configure(bg ="Red")
root.geometry("300x400")
#Function to open new window 
def openNewWindow() :
  newWindow = tk.Toplevel(root) 
  newWindow.title("Second Window")
  newWindow.geometry("500x500")
  newWindow.configure(bg="Yellow")
  LabelTwo = tk.Label(newWindow, text="This is the second window")
  LabelTwo.pack()

button = tk.Button(root,text="Click to Open New Window",command=openNewWindow)
button.pack()

root.mainloop()