import tkinter as tk
from tkinter import messagebox

root = tk.Tk()

# Task 5.1 & 5.2
def calculate(operation):
    try:
        if entryNum1.get() == "" or entryNum2.get() == "":
            messagebox.showerror("Error", "Enter both numbers")
            return
        num1 = float(entryNum1.get())
        num2 = float(entryNum2.get())
        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            if num2 == 0:
                messagebox.showerror("Error", "Cannot divide by zero")
                return
            result = num1 / num2
        labelCalcResult.config(text=f"Result: {result}")
    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers")

tk.Label(root, text="Number 1:").pack()
entryNum1 = tk.Entry(root)
entryNum1.pack()
tk.Label(root, text="Number 2:").pack()
entryNum2 = tk.Entry(root)
entryNum2.pack()

frameButtons = tk.Frame(root)
frameButtons.pack()
tk.Button(frameButtons, text="Add", command=lambda: calculate("add")).grid(row=0, column=0)
tk.Button(frameButtons, text="Subtract", command=lambda: calculate("subtract")).grid(row=0, column=1)
tk.Button(frameButtons, text="Multiply", command=lambda: calculate("multiply")).grid(row=1, column=0)
tk.Button(frameButtons, text="Divide", command=lambda: calculate("divide")).grid(row=1, column=1)

labelCalcResult = tk.Label(root, text="Result: ")
labelCalcResult.pack()

# Task 5.3
def calculateGrade():
    try:
        marks1 = float(entryMarks1.get())
        marks2 = float(entryMarks2.get())
        marks3 = float(entryMarks3.get())
        total = marks1 + marks2 + marks3
        percentage = (total / 300) * 100
        if percentage >= 80:
            grade = "A"
        elif percentage >= 60:
            grade = "B"
        elif percentage >= 40:
            grade = "C"
        else:
            grade = "F"
        messagebox.showinfo("Result", f"Total: {total}\nPercentage: {percentage:.2f}%\nGrade: {grade}")
    except ValueError:
        messagebox.showerror("Error", "Enter valid marks")

tk.Label(root, text="Subject 1:").pack()
entryMarks1 = tk.Entry(root)
entryMarks1.pack()
tk.Label(root, text="Subject 2:").pack()
entryMarks2 = tk.Entry(root)
entryMarks2.pack()
tk.Label(root, text="Subject 3:").pack()
entryMarks3 = tk.Entry(root)
entryMarks3.pack()
tk.Button(root, text="Calculate", command=calculateGrade).pack()

root.mainloop()
