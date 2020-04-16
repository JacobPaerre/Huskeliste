import tkinter as tk
from tkinter import *
import os

root = tk.Tk()

# Baggrund
canvas = tk.Canvas(root, height=800, width=800, bg="#404040")
canvas.pack()

# Venstre del af UI
frame = tk.Frame(root, bg="#1D4147")
frame.place(relwidth=0.225, relheight=1)

# Split mellem højre og venstre
frame = tk.Frame(root, bg="#227373")

# Højre del af UI (toppen)
frame = tk.Frame(root, bg="#208C81")
frame.place(x=190, relwidth=1, relheight=0.08)


#Højre del af UI (bunden)

# Starter UI'en
root.mainloop()
