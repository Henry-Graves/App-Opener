#   Inspired by Dev Ed, https://www.youtube.com/watch?v=jE-SpRI3K5g.
#   Design and functionality improved by Henry Graves.

import os
import tkinter as tk
import tkinter.font as TkFont
from tkinter import *
from tkinter import filedialog, Text
from pathlib import Path
#from tkinter.ttk import *

root = tk.Tk()
root.title('App Opener')
#root.iconbitmap(r'C:\Users\henry\Downloads\171127-200.ico')
apps = []
appsNoFilepath = []
font = TkFont.Font(family="Arial", size=10, weight="bold")
menuFont = TkFont.Font(family="Arial", size=10)
menubar = Menu(root)

# Reads our previous save of apps, converts to CSV array
if os.path.isfile('appOpener.txt'):
    with open('appOpener.txt', 'r') as file:
        tempApps = file.read()
        apps = tempApps.split(',')
        apps = [i for i in apps if i.strip()] # Gets rid of empty lines

def addApp():
    # Clears the previous apps from screen, they will be re-added later
    for widget in frame.winfo_children():
        widget.destroy()

    filename = filedialog.askopenfilename(initialdir="/", title="Select File:",
        filetypes=(("executables", "*.exe"), ("all files", "*.*"))) # Defaults to showing the .exe files in "open file" browser

    # Adds nothing if user doesn't select a file
    if (filename != ""):
        # Create simplified app list and display it
        apps.append(filename)
        p = Path(filename)
        name = p.name.capitalize()
        name = name.removesuffix('.exe')
        appsNoFilepath.append(name)

    for app in appsNoFilepath:
        label = tk.Label(frame, text=app, font=font)
        label.pack(fill=BOTH)

def clearApps():
    # if (click yes)
        # (put the following code in this indent)
    for widget in frame.winfo_children():
        widget.destroy()

    apps.clear()
    appsNoFilepath.clear()

def runApps():
    for app in apps:
        os.startfile(app)
    root.destroy() # Close App Opener upon running selected apps

def changeProfile():
    print("change")

def addProfile():
    print("add")

def deleteProfile():
    print("delete")

# Draw main canvas and frame
canvas = tk.Canvas(root, height=478, width=314, bg="#ffffff")
canvas.pack(fill=BOTH, expand=TRUE)
frame = tk.Frame(root, bg="#ffffff")
frame.place(relwidth=0.8, relheight=0.6, relx=0.1, rely=0.1)

# Buttons
runApps = tk.Button(root, text="Run Apps", font=font, width=10, padx=10, pady=5, bd=1, relief="groove",
    fg="#ffffff", bg="#55acee", command=runApps)
runApps.pack(side="right", fill=Y)

addApp = tk.Button(root, text="Add App", font=font, width=10, padx=10, pady=5, bd=1, relief="groove",
    fg="#ffffff", bg="#55acee", command=addApp)
addApp.pack(side="right", fill=Y)

clearApps = tk.Button(root, text="Clear Apps", font=font, width=10, padx=10, pady=5,bd=1, relief="groove",
    fg="#ff4f4b", bg="#55acee", activebackground="red", command=clearApps)
clearApps.pack(side="right", fill=Y)

# Profiles menu in top menu bar
profile = Menu(menubar, activebackground="#55acee", font=menuFont, relief="groove", tearoff=0)
profileList = Menu(menubar, activebackground="#55acee", font=menuFont, relief="groove", tearoff=0)
menubar.add_cascade(label='Profile', menu=profile)
profile.add_cascade(label='Change Profile', menu=profileList)
# TODO: for profile in profiles: profileList.add_command(label=profile, command=changeProfile(profile))
profileList.add_command(label='test', command=changeProfile)
profile.add_separator()
profile.add_command(label='Add Profile', command=addProfile)
profile.add_command(label='Delete Profile', command=deleteProfile)
root.config(menu=menubar)

# Create simplified app list and display it
for i in range(0, len(apps)):
    p = Path(apps[i])
    name = p.name.capitalize()
    name = name.removesuffix('.exe')
    appsNoFilepath.append(name)

for app in appsNoFilepath:
    label = tk.Label(frame, text=app, font=font)
    label.pack(fill=BOTH)

root.mainloop()

# Save file of chosen apps
with open('appOpener.txt', 'w') as file:
    print("Saved apps:")
    for app in apps:
        print(app)
        file.write(app + ',')