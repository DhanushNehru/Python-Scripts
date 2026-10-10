import tkinter as tk
from tkinter import filedialog

def save_file():
    file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file:
        with open(file, 'w') as f:
            f.write(text_area.get(1.0, tk.END))

def open_file():
    file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file:
        with open(file, 'r') as f:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, f.read())

root = tk.Tk()
root.title("Notepad")
text_area = tk.Text(root, wrap='word')
text_area.pack(expand='yes', fill='both')

menu = tk.Menu(root)
root.config(menu=menu)
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save As", command=save_file)

root.mainloop()
