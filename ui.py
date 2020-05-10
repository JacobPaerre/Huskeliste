try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk
import os
import sqlite3

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
# elements=[(id), listIndex, elementTitle, elementContent]

class NewRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-alpha', 0.0)

class App(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        # Borderless window initialization
        self.windowed = True
        self.overrideredirect(1)
        self.attributes('-topmost', 1)
        self.windowSize = "600x400"
        self.windowX = 0
        self.windowY = 0
        self.minsize(600,400)
        self.geometry(self.windowSize)

        # Database stuff
        self.lists = []
        self.listElements = []
        self.openListId = -1

        # Initialize widgets
        self.createWidgets()

        # Load in lists from database
        self.updateLists()

    # Initialize widgets
    def createWidgets(self):
        # Body
        self.body = tk.Frame(self, bg="#75A08D")
        self.body.pack(fill=tk.BOTH, expand=True)

        # Topbar
        self.topBar = tk.Frame(self.body, bg="#75A89F")
        self.topBar.pack(side=tk.TOP, fill=tk.X)
        self.topBar.bind("<ButtonPress-1>", self.start_move)
        self.topBar.bind("<ButtonRelease-1>", self.stop_move)
        self.topBar.bind("<B1-Motion>", self.do_move)

        # Quit button
        self.quitButtonImage = tk.PhotoImage(file="./res/quitIcon25Light.png")
        self.quitBtn = tk.Button(self.topBar, command=self.onClose, image=self.quitButtonImage, text="X", font=("Ubuntu", 14), fg="white", bg=self.topBar["bg"], bd=0)
        self.quitBtn.pack(side=tk.RIGHT)

        # Windowedmode button
        self.fullscreenButtonImage = tk.PhotoImage(file="./res/fullscreenIcon25Light.png")
        self.windowedBtn = tk.Button(self.topBar, command=self.toggleWindowed, image=self.fullscreenButtonImage, text="☐", font=("Ubuntu", 14), fg="white", bg=self.topBar["bg"], bd=0)
        self.windowedBtn.pack(side=tk.RIGHT)

        # Venstre del af UI
        self.sidebar = tk.Frame(self.body, padx=60, bg="#1D4147")
        self.sidebar.pack(fill=tk.Y, side=tk.LEFT)

        self.logo = tk.Label(self.sidebar, text="Huskeliste", bg="#1D4147",fg="white", font=("Ubuntu, 32"),)
        self.logo.pack(pady=25)

        self.addlistbutton = tk.Button(self.sidebar, text="Ny liste", command=self.openListAdd, width="12", font=("Ubuntu 16"), bg="#208C81", bd=0, fg="white")
        self.addlistbutton.pack(pady=20)

        self.listnavcontainer = tk.Frame(self.sidebar, bg="#1D4147")
        self.listnavcontainer.pack()

        # Split mellem højre og venstre
        self.sidebarsplit = tk.Frame(self.body, width=20,bg="#227373")
        self.sidebarsplit.pack(fill=tk.Y, side=tk.LEFT)

        # Højre del af UI (bunden)
        self.elementdesk = tk.Frame(self.body, bg="#404040")
        self.elementdesk.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.addelementbutton = tk.Button(self.elementdesk, state=tk.DISABLED, text="Nyt punkt", command=self.openElementAdd, width="12", font=("Ubuntu 16"), bg="#208C81", bd=0, fg="white")
        self.addelementbutton.pack(pady=20)

        self.elementContainer = tk.Frame(self.elementdesk, bg="#404040")
        self.elementContainer.pack(fill=tk.BOTH, side=tk.TOP, expand=True)


        # Resizing
        self.resizer = ttk.Sizegrip(self)
        self.resizer.place(relx=1.0, rely=1.0, anchor="se")
        self.resizer.bind("<B1-Motion>", self.do_resize)

    # Closing app
    def onClose(self, event=None):
        self.master.destroy()

    # Toggle windowed
    def toggleWindowed(self):
        if self.windowed:
            self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(),self.winfo_screenheight()))
        else:
            self.geometry(self.windowSize+"+{0}+{1}".format(self.windowX, self.windowY))
        self.windowed = not self.windowed

    # Moving window
    def start_move(self, event):
        if self.windowed:
            self.x = event.x
            self.y = event.y

    def stop_move(self, event):
        if self.windowed:
            self.x = None
            self.y = None

    def do_move(self, event):
        if self.windowed:
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.winfo_x() + deltax
            y = self.winfo_y() + deltay
            self.geometry(f"+{x}+{y}")
            self.windowX = x
            self.windowY = y

    # Resizing window
    def do_resize(self, event):
        if not self.windowed:
            self.windowed = True
        x1 = self.winfo_pointerx()
        y1 = self.winfo_pointery()
        x0 = self.winfo_rootx()
        y0 = self.winfo_rooty()
        self.windowSize = "{0}x{1}".format(x1-x0,y1-y0)
        self.geometry(self.windowSize)
        return

    # Open window for creating new list
    def openListAdd(self):
        self.newlist = tk.Tk()
        self.newlist.geometry("200x50")
        self.newlist.title("Create a new list")
        self.newlist.attributes('-topmost', 1)

        tk.Label(self.newlist, text="List name:").grid(row=0)
        tk.Label(self.newlist, text=" ").grid(row=1)

        self.entrylistname = tk.StringVar(self.newlist)
        entry1 = tk.Entry(self.newlist, textvariable = self.entrylistname)
        tk.Button(self.newlist, text="Create list", command=self.addList).grid(row=1, column=1)

        entry1.grid(row=0, column=1)
        entry1.bind('<Return>', self.addList)
        entry1.focus_set()
        self.newlist.focus_force()

    # Add list to database and update displayed lists
    def addList(self, event=None):

        name = self.entrylistname.get()

        if name.isspace() == True:
            name = "Untitled list"
        if name == "":
            name = "Untitled list"

        commandDatabase('INSERT INTO lists(listTitle) VALUES(\'{0}\')'.format(name))
        self.updateLists()

        self.newlist.destroy()

    # Update displayed lists
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

    # Open window for creating new element
    def openElementAdd(self):
        self.newelement = tk.Tk()
        self.newelement.geometry("200x130")
        self.newelement.title("Create a new element")
        self.newelement.attributes('-topmost', 1)

        tk.Label(self.newelement, text="Element name:").grid(row=0)
        tk.Label(self.newelement, text=" ").grid(row=1)

        self.entryelementname = tk.StringVar(self.newelement)
        entry1 = tk.Entry(self.newelement, textvariable = self.entryelementname)

        tk.Label(self.newelement, text="Element notes:").grid(row=2)
        tk.Label(self.newelement, text=" ").grid(row=3)

        self.entryelementcontent = tk.StringVar(self.newelement)
        entry2 = tk.Entry(self.newelement, textvariable = self.entryelementcontent)

        tk.Button(self.newelement, text="Create element", command=self.addElement).grid(row=4, column=0, columnspan=2)

        entry1.grid(row=0, column=1)
        entry1.focus_set()

        entry2.grid(row=2, column=1)
        entry2.bind('<Return>', self.addElement)
        self.newelement.focus_force()

    # Add list to database and update displayed elements
    def addElement(self, event=None):

        name = self.entryelementname.get()
        content = self.entryelementcontent.get()

        if name.isspace() == True:
            name = "Untitled element"
        if name == "":
            name = "Untitled element"

        commandDatabase('INSERT INTO elements(listIndex, elementTitle, elementContent) VALUES(\'{0}\',\'{1}\',\'{2}\')'.format(self.openListId, name, content))
        self.updateElements()

        self.newelement.destroy()

    # Update displayed elements
    def updateElements(self):
        for e in self.listElements:
            e.destroy()
        del self.listElements[:]
        conn = sqlite3.connect("./db/listDatabase.db")
        c = conn.cursor()
        c.execute('SELECT * FROM elements WHERE listindex = {0}'.format(self.openListId))
        dbelements = c.fetchall()
        conn.close()
        for e in dbelements:
            self.listElements.append(ListElement(self.elementContainer, e[0], e[1], e[2], e[3]))

# Sqlite command for database
def commandDatabase(sqlCommand):
    conn = sqlite3.connect("./db/listDatabase.db")
    c = conn.cursor()
    c.execute(sqlCommand)
    conn.commit()
    conn.close()

# List class for lists loaded from database
class List():
    def __init__(self, master, listid, title="Untitled List"):
        self.id = listid
        self.title = title
        
        self.frame = tk.Frame(master, bg=master["bg"])
        self.frame.pack(fill=tk.X)

        self.liste = tk.Button(self.frame, command=self.showListElements, text=self.title, font=("Ubuntu", 14), fg="white", bg="#1D4147", bd=0)
        self.liste.pack(side=tk.LEFT, expand=True)
        
        self.quitButtonImage = tk.PhotoImage(file="./res/quitIcon25Light.png")
        self.removeList = tk.Button(self.frame, command=self.removeListFromDatabase, text="X", image=self.quitButtonImage, font=("Ubuntu", 14), fg="white", bg="#1D4147", bd=0)
        self.removeList.pack(side=tk.RIGHT)

        self.editButtonImage = tk.PhotoImage(file="./res/editIcon25Green.png")
        self.editList = tk.Button(self.frame, command=self.openTitleEdit, text="Edit", image=self.editButtonImage, font=("Ubuntu", 14), fg="white", bg="#1D4147", bd=0)
        self.editList.pack(side=tk.RIGHT)

    def showListElements(self, event=None):
        for l in app.lists:
            l.liste["bg"] = "#1D4147"
        self.liste["bg"] = "#208C81"
        app.openListId = self.id
        app.addelementbutton["state"] = "normal"
        app.updateElements()

    def openTitleEdit(self):
        self.editList = tk.Tk()
        self.editList.geometry("200x50")
        self.editList.title("Edit list name")
        self.editList.attributes('-topmost', 1)

        tk.Label(self.editList, text="List name:").grid(row=0)
        tk.Label(self.editList, text=" ").grid(row=1)

        self.entrylistname = tk.StringVar(self.editList)
        entry1 = tk.Entry(self.editList, textvariable = self.entrylistname)
        tk.Button(self.editList, text="Submit name", command=self.editListInDatabase).grid(row=1, column=1)

        entry1.grid(row=0, column=1)
        entry1.insert(0, self.title)
        entry1.bind('<Return>', self.editListInDatabase)
        entry1.focus_set()
        self.editList.focus_force()

    # Edit list title
    def editListInDatabase(self, event=None):
        name = self.entrylistname.get()

        if name.isspace() == True:
            name = "Untitled list"
        if name == "":
            name = "Untitled list"

        commandDatabase("UPDATE lists SET listTitle = \'{0}\' WHERE id = {1}".format(name, self.id))
        app.updateLists()

        self.editList.destroy()

    # Removes list from database (shocker)
    def removeListFromDatabase(self, event=None):
        commandDatabase('DELETE FROM lists WHERE id = {0}'.format(self.id))
        app.updateLists()
    
    # Remove all widgets created by this object
    def destroy(self):
        app.openListId = -1
        app.addelementbutton["state"] = "disabled"
        self.liste.destroy()
        self.frame.destroy()



# Element class for elements loaded from database
class ListElement():
    def __init__(self, master, elementid, listId, title="Untitled Element", elementContent=""):
        self.id = elementid
        self.listId = listId
        self.title = title
        self.elementContent = elementContent
        
        self.frame = tk.Frame(master, bg="#EEE")
        self.frame.pack(fill=tk.X)

        self.quitButtonImage = tk.PhotoImage(file="./res/quitIcon25Dark.png")
        self.removeElement = tk.Button(self.frame, command=self.removeElementFromDatabase, text="X", image=self.quitButtonImage, font=("Ubuntu", 14), bg=self.frame["bg"], bd=0)
        self.removeElement.pack(side=tk.RIGHT)

        self.editButtonImage = tk.PhotoImage(file="./res/editIcon25Green.png")
        self.editElementButton = tk.Button(self.frame, command=self.openElementEdit, text="Edit", image=self.editButtonImage, font=("Ubuntu", 14), bg=self.frame["bg"], bd=0)
        self.editElementButton.pack(side=tk.RIGHT)

        self.titleLabel = tk.Label(self.frame, text=self.title, font=("Ubuntu", 16))
        self.titleLabel.pack(side=tk.TOP, fill=tk.X, expand=True)

        self.contentLabel = tk.Label(self.frame, text=self.elementContent, font=("Ubuntu", 12))
        self.contentLabel.pack(side=tk.TOP, fill=tk.X, expand=True)

    def openElementEdit(self):
        self.editElement = tk.Tk()
        self.editElement.geometry("200x130")
        self.editElement.title("Create a new element")
        self.editElement.attributes('-topmost', 1)

        tk.Label(self.editElement, text="Element name:").grid(row=0)
        tk.Label(self.editElement, text=" ").grid(row=1)

        self.entryelementname = tk.StringVar(self.editElement)
        entry1 = tk.Entry(self.editElement, textvariable = self.entryelementname)

        tk.Label(self.editElement, text="Element notes:").grid(row=2)
        tk.Label(self.editElement, text=" ").grid(row=3)

        self.entryelementcontent = tk.StringVar(self.editElement)
        entry2 = tk.Entry(self.editElement, textvariable = self.entryelementcontent)

        tk.Button(self.editElement, text="Create element", command=self.editElementInDatabase).grid(row=4, column=0, columnspan=2)

        entry1.grid(row=0, column=1)
        entry1.focus_set()

        entry2.grid(row=2, column=1)
        entry2.bind('<Return>', self.editElementInDatabase)
        self.editElement.focus_force()

    # Edit element
    def editElementInDatabase(self, event=None):
        name = self.entryelementname.get()
        content = self.entryelementcontent.get()

        if name.isspace() == True:
            name = "Untitled element"
        if name == "":
            name = "Untitled element"

        commandDatabase("UPDATE elements SET elementTitle = \'{0}\' WHERE id = {1}".format(name, self.id))
        commandDatabase("UPDATE elements SET elementContent = \'{0}\' WHERE id = {1}".format(content, self.id))
        app.updateElements()

        self.editElement.destroy()

    # Removes element from database (shocker)
    def removeElementFromDatabase(self, event=None):
        commandDatabase('DELETE FROM elements WHERE id = {0}'.format(self.id))
        app.updateElements()
    
    # Remove all widgets created by this object
    def destroy(self):
        self.titleLabel.destroy()
        self.frame.destroy()

if __name__ == "__main__":
    root = NewRoot()
    root.lower()
    root.iconify()
    root.title("Application")

    app = App(root)
    app.mainloop()