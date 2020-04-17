import tkinter as tk
import os

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("576x324")
        self.root.overrideredirect(0)
        self.windowed = True

        # Bar til windowed mode og muligvis exit
        self.managementbar = tk.Frame(self.root, height=25, bg="#75A08D")
        self.managementbar.pack(fill=tk.X, side=tk.TOP)

        self.windowbutton = tk.Button(self.managementbar, text="Toggle window", command=self.toggleWindow)
        self.windowbutton.pack(side=tk.RIGHT)

        # Venstre del af UI
        self.sidebar = tk.Frame(self.root, padx=60, bg="#1D4147")
        self.sidebar.pack(fill=tk.Y, side=tk.LEFT)

        self.logo = tk.Label(self.sidebar, text="Huskeliste", bg="#1D4147",fg="black", font=("Ubuntu, 24"),)
        self.logo.pack()

        # Split mellem højre og venstre
        self.sidebarsplit = tk.Frame(self.root, width=20,bg="#227373")
        self.sidebarsplit.pack(fill=tk.Y, side=tk.LEFT)

        # Højre del af UI (toppen)
        self.topbar = tk.Frame(self.root, height=100, bg="#208C81")
        self.topbar.pack(fill=tk.X, side=tk.TOP)

        # Højre del af UI (bunden)
        self.listdesk = tk.Frame(self.root, bg="#404040")
        self.listdesk.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    def toggleWindow(self):
            if self.windowed:
                self.windowed = False
                self.root.geometry(str(self.root.winfo_screenwidth())+"x"+str(self.root.winfo_screenheight())+"+0+0")
                self.root.overrideredirect(1)
            else:
                self.windowed = True
                self.root.minsize(576, 324)
                self.root.geometry("576x324")
                self.root.overrideredirect(0)

app = App()
# Starter UI'en
app.root.mainloop()
