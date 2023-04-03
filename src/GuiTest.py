#from tkinter import * # PEP8: `import *` is not preferred
import tkinter as tk
import time

# --- function ---

def add_line():
    listbox.insert('end', time.strftime("%H:%M:%S"))
    root.after(1000, add_line)  # run `add_line` again after 1000ms (1s)

# --- main ---

root = tk.Tk()

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side='right', fill='y')

listbox = tk.Listbox(root, yscrollcommand=scrollbar.set)
listbox.pack(side='left', fill='both')

scrollbar.config(command=listbox.yview)

add_line()  # run `add_line` first time

root.mainloop()
