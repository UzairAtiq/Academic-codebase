import tkinter as tk

root = tk.Tk()

# Task 1.1
windowTitle = "Lab 1"
root.title(windowTitle)
root.geometry("500x400")
root.config(bg="lightblue")
root.resizable(False, False)

# Task 1.2
def openSecondWindow():
    secondWindow = tk.Toplevel(root)
    secondWindow.title("Second Window")
    secondWindow.config(bg="lightgreen")

tk.Button(root, text="Open Second Window", command=openSecondWindow).pack()

root.mainloop()