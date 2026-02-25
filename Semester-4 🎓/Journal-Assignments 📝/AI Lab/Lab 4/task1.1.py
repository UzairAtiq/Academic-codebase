import tkinter as tk

root = tk.Tk()

#Task 1.1 
root.geometry("300x400")  #--Set WIndow Size 
root.configure(bg="Purple") #--Change BG Color  
root.resizable(False,False) #-- Disable resizing
#--Dynamiz resizing 
width = 300
height = 400
root.geometry(f"{height}x{width}")


root.mainloop()