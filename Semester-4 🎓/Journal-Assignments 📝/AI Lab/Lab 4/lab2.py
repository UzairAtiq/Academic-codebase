import tkinter as tk

root = tk.Tk()

isChanged = False
counter = 0

# Task 2.1
def toggleText():
    global isChanged
    if isChanged:
        labelToggle.config(text="Original Text")
    else:
        labelToggle.config(text="Text Changed!")
    isChanged = not isChanged

labelToggle = tk.Label(root, text="Original Text")
labelToggle.pack()
tk.Button(root, text="Toggle", command=toggleText).pack()

# Task 2.2
def incrementCounter():
    global counter
    counter += 1
    labelCounter.config(text=f"Count: {counter}")

labelCounter = tk.Label(root, text=f"Count: {counter}")
labelCounter.pack()
tk.Button(root, text="Increment", command=incrementCounter).pack()

root.mainloop()
