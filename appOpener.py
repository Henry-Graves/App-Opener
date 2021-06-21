#   Inspired by Dev Ed, https://www.youtube.com/watch?v=jE-SpRI3K5g.
#   Design and functionality improved by Henry Graves.

import tkinter as tk
from tkinter import filedialog, Text
import os

root = tk.Tk()
apps = []

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

    apps.append(filename)

    # Displays the list of app names
    for app in apps:
        label = tk.Label(frame, text=app, bg="gray")
        label.pack()

def clearApps():
    for widget in frame.winfo_children():
        widget.destroy()

    apps.clear()

def runApps():
    for app in apps:
        os.startfile(app)

# Draw main canvas and frame
canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
canvas.pack()
frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.6, relx=0.1, rely=0.1)

# Buttons
addApp = tk.Button(root, text="Add App", padx=10, pady=5, fg="white", bg="#263D42", command=addApp)
addApp.pack()

runApps = tk.Button(root, text="Run Apps", padx=10, pady=5, fg="green", bg="#263D42", command=runApps)
runApps.pack()

clearApps = tk.Button(root, text="Clear Apps", padx=10, pady=5, fg="red", bg="#263D42", command=clearApps)
clearApps.pack()

# Draw app list
for app in apps:
    label = tk.Label(frame, text=app)
    label.pack()

root.mainloop()

# Save file of chosen apps
with open('appOpener.txt', 'w') as file:
    print("Saved apps:")
    for app in apps:
        print(app)
        file.write(app + ',')