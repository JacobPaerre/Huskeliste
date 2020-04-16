import tkinter as tk
from tkinter import *
import os

root = tk.Tk()

# Baggrund
canvas = tk.Canvas(root, height=800, width=800, bg="white")
canvas.pack()

# Venstre del af UI
frame = tk.Frame(root, bg="#1D4147")
frame.place(relwidth=0.225, relheight=1)

# Split mellem højre og venstre
frame = tk.Frame(root, bg="#227373")
frame.place(x=170, relwidth=0.03, relheight=1)

# Højre del af UI (toppen)
frame = tk.Frame(root, bg="#208C81")
frame.place(x=194, relwidth=1, relheight=0.08)

# Højre del af UI (bunden)
frame = tk.Frame(root, bg="#404040")
frame.place(x=194, y=64, relwidth=1, relheight=1)


# Starter UI'en
root.mainloop()
