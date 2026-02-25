import tkinter as tk
from tkinter import messagebox

root = tk.Tk()

isDark = False

# Dark mode toggle
def toggleDarkMode():
    global isDark
    if not isDark:
        root.config(bg="#2b2b2b")
        buttonDark.config(text="Light Mode")
    else:
        root.config(bg="white")
        buttonDark.config(text="Dark Mode")
    isDark = not isDark

# Menu bar
def exitApp():
    root.quit()

menuBar = tk.Menu(root)
root.config(menu=menuBar)
fileMenu = tk.Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Exit", command=exitApp)

buttonDark = tk.Button(root, text="Dark Mode", command=toggleDarkMode)
buttonDark.pack()

# Image display
try:
    myImage = tk.PhotoImage(file="image.png")
    tk.Label(root, image=myImage).pack()
except:
    tk.Label(root, text="No image.png").pack()

# Prime checker
def isPrime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def checkPrime():
    try:
        userNumber = int(entryPrime.get())
        if isPrime(userNumber):
            messagebox.showinfo("Result", f"{userNumber} is Prime")
        else:
            messagebox.showinfo("Result", f"{userNumber} is NOT Prime")
    except ValueError:
        messagebox.showerror("Error", "Enter valid number")

tk.Label(root, text="Enter number:").pack()
entryPrime = tk.Entry(root)
entryPrime.pack()
tk.Button(root, text="Check Prime", command=checkPrime).pack()

root.mainloop()
