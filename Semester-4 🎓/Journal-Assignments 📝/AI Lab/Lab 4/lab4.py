import tkinter as tk

root = tk.Tk()

genderVar = tk.StringVar(value="Male")

# Task 4.1
def loginUser():
    userName = entryUsername.get()
    labelLoginResult.config(text=f"Login: {userName}")

def clearLogin():
    entryUsername.delete(0, tk.END)
    entryPassword.delete(0, tk.END)
    labelLoginResult.config(text="")

tk.Label(root, text="Username:").grid(row=0, column=0)
entryUsername = tk.Entry(root)
entryUsername.grid(row=0, column=1)
tk.Label(root, text="Password:").grid(row=1, column=0)
entryPassword = tk.Entry(root, show="*")
entryPassword.grid(row=1, column=1)
tk.Button(root, text="Login", command=loginUser).grid(row=2, column=0)
tk.Button(root, text="Clear", command=clearLogin).grid(row=2, column=1)
labelLoginResult = tk.Label(root, text="")
labelLoginResult.grid(row=3, column=0, columnspan=2)

# Task 4.2
def submitRegistration():
    userName = entryRegName.get()
    userEmail = entryRegEmail.get()
    userAge = entryRegAge.get()
    userGender = genderVar.get()
    labelRegResult.config(text=f"{userName} - {userGender}")

tk.Label(root, text="Name:").grid(row=4, column=0)
entryRegName = tk.Entry(root)
entryRegName.grid(row=4, column=1)
tk.Label(root, text="Email:").grid(row=5, column=0)
entryRegEmail = tk.Entry(root)
entryRegEmail.grid(row=5, column=1)
tk.Label(root, text="Age:").grid(row=6, column=0)
entryRegAge = tk.Entry(root)
entryRegAge.grid(row=6, column=1)
tk.Label(root, text="Gender:").grid(row=7, column=0)
frameGender = tk.Frame(root)
frameGender.grid(row=7, column=1)
tk.Radiobutton(frameGender, text="Male", variable=genderVar, value="Male").pack(side=tk.LEFT)
tk.Radiobutton(frameGender, text="Female", variable=genderVar, value="Female").pack(side=tk.LEFT)
tk.Button(root, text="Submit", command=submitRegistration).grid(row=8, column=0, columnspan=2)
labelRegResult = tk.Label(root, text="")
labelRegResult.grid(row=9, column=0, columnspan=2)

root.mainloop()
