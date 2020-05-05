import tkinter as tk
import os
import sqlite3
from string import Template

# STYLES TIL GUI

# Borderless window movement code from Bryan Oakley on stackoverflow: https://stackoverflow.com/a/4055612/13319955

# DATABASE SETUP
# conn = sqlite3.connect("./db/listDatabase.db")
# c = conn.cursor()
# c.execute("""CREATE TABLE lists (
#         id integer PRIMARY KEY,
#         listTitle text
#         )
#         """)
# c.execute("""CREATE TABLE elements (
#         id integer PRIMARY KEY,
#         listIndex integer,
#         elementTitle text,
#         elementContent text
#         )
#         """)
# conn.commit()
# conn.close()
#
# lists=[(id), listTitle]
# elements=[(id), elementIndex, elementTitle, elementContent]

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("576x324")
        self.root.overrideredirect(1)
        self.windowed = True
        self.lists = []

        # Bar til windowed mode og muligvis exit
        self.managementbar = tk.Frame(self.root, height=25, bg="#75A08D")
        self.managementbar.pack(fill=tk.X, side=tk.TOP)

        self.managementbar.bind("<ButtonPress-1>", self.StartMove)
        self.managementbar.bind("<ButtonRelease-1>", self.StopMove)
        self.managementbar.bind("<B1-Motion>", self.OnMotion)

        self.quitbutton = tk.Button(self.managementbar, text="Exit", command=self.root.destroy)
        self.quitbutton.pack(side=tk.RIGHT)

        self.windowbutton = tk.Button(self.managementbar, text="Toggle window", command=self.toggleWindow)
        self.windowbutton.pack(side=tk.RIGHT)

        # Venstre del af UI
        self.sidebar = tk.Frame(self.root, padx=60, bg="#1D4147")
        self.sidebar.pack(fill=tk.Y, side=tk.LEFT)

        self.logo = tk.Label(self.sidebar, text="Huskeliste", bg="#1D4147",fg="white", font=("Ubuntu, 32"),)
        self.logo.pack()

        self.addbutton = tk.Button(self.sidebar, text="Ny liste", command=self.openListAdd, width="12", font=("Ubuntu 16"), bg="#208C81", bd=0, fg="white")
        self.addbutton.pack()

        self.listnavcontainer = tk.Frame(self.sidebar, bg="#1D4147")
        self.listnavcontainer.pack()

        # Split mellem højre og venstre
        self.sidebarsplit = tk.Frame(self.root, width=20,bg="#227373")
        self.sidebarsplit.pack(fill=tk.Y, side=tk.LEFT)

        # Højre del af UI (toppen)
        self.topbar = tk.Frame(self.root, height=100, bg="#208C81")
        self.topbar.pack(fill=tk.X, side=tk.TOP)

        # Højre del af UI (bunden)
        self.listdesk = tk.Frame(self.root, bg="#404040")
        self.listdesk.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        # Load in lists from database
        self.updateLists()

    def toggleWindow(self):
        if self.windowed:
            self.windowed = False
            self.root.geometry(str(self.root.winfo_screenwidth())+"x"+str(self.root.winfo_screenheight())+"+0+0")
        else:
            self.windowed = True
            self.root.minsize(576, 324)
            self.root.geometry("576x324")

    def openListAdd(self):

        self.newlist = tk.Tk()
        self.newlist.geometry("200x50")
        self.newlist.title("Create a new list")

        tk.Label(self.newlist, text="List name:").grid(row=0)
        tk.Label(self.newlist, text=" ").grid(row=1)

        self.entrylistname = tk.StringVar(self.newlist)
        entry1 = tk.Entry(self.newlist, textvariable = self.entrylistname)
        tk.Button(self.newlist, text="Create list", command=self.addList).grid(row=1, column=1)

        entry1.grid(row=0, column=1)

    def commandDatabase(self, sqlCommand):
        conn = sqlite3.connect("./db/listDatabase.db")
        c = conn.cursor()
        c.execute(sqlCommand)
        conn.commit()
        conn.close()

    def addList(self):

        name = self.entrylistname.get()

        if name.isspace() == True:
            name = "Untitled list"
        if name == "":
            name = "Untitled list"

        self.commandDatabase(Template('INSERT INTO lists(listTitle) VALUES(\'$title\')').substitute(title=name))
        self.updateLists()

        self.newlist.destroy()

    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None

    def OnMotion(self, event):
        if self.windowed:
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.root.winfo_x() + deltax
            y = self.root.winfo_y() + deltay
            self.root.geometry("+%s+%s" % (x, y))

    def updateLists(self):
        for l in self.lists:
            l.destroy()
        del self.lists[:]
        conn = sqlite3.connect("./db/listDatabase.db")
        c = conn.cursor()
        c.execute('SELECT * FROM lists')
        dblists = c.fetchall()
        conn.close()
        for l in dblists:
            self.lists.append(List(self.listnavcontainer, l[0], l[1]))

class List():
    def __init__(self, master, listid, title="Untitled List"):
        self.id = listid
        self.title = title
        
        self.frame = tk.Frame(master)
        self.frame.pack()

        self.liste = tk.Button(self.frame, text=self.title, font=("Ubuntu", 14), fg="white", bg="#1D4147", bd=0)
        self.liste.pack()
    
    def destroy(self):
        self.liste.destroy()
        self.frame.destroy()

app = App()
# Starter UI'en
app.root.mainloop()