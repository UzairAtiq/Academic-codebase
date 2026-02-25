import tkinter as tk

root = tk.Tk()

# Task 3.1
def greetUser():
    userName = entryName.get()
    labelGreeting.config(text=f"Hello {userName}, Welcome to AI Lab!")

tk.Label(root, text="Enter name:").pack()
entryName = tk.Entry(root)
entryName.pack()
tk.Button(root, text="Submit", command=greetUser).pack()
labelGreeting = tk.Label(root, text="")
labelGreeting.pack()

# Task 3.2
def validatePassword(event=None):
    userPassword = entryPassword.get()
    if userPassword == "admin123":
        labelResult.config(text="Access Granted")
    else:
        labelResult.config(text="Access Denied")

tk.Label(root, text="Enter password:").pack()
entryPassword = tk.Entry(root, show="*")
entryPassword.pack()
tk.Button(root, text="Submit", command=validatePassword).pack()
labelResult = tk.Label(root, text="")
labelResult.pack()

# Task 3.3
entryPassword.bind("<Return>", validatePassword)

root.mainloop()
