import tkinter as tk
from tkinter import ttk

def toggle_dark_mode():
    if root['bg'] == 'black':
        # Switch to light mode
        root.config(bg='white')
        label.config(bg='white', fg='black')
        button.config(bg='lightgray', fg='black')
    else:
        # Switch to dark mode
        root.config(bg='black')
        label.config(bg='black', fg='white')
        button.config(bg='gray', fg='white')

root = tk.Tk()
root.title("Tkinter Dark Mode Example")
root.geometry("300x200")

# Set initial background color (light mode)
root.config(bg='white')

# Create label and button
label = tk.Label(root, text="Dark Mode Toggle", bg='white', fg='black', font=("Arial", 14))
label.pack(pady=20)

button = tk.Button(root, text="Toggle Dark Mode", command=toggle_dark_mode, bg='lightgray', fg='black')
button.pack(pady=10)

root.mainloop()
