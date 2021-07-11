#   Inspired by Dev Ed, https://www.youtube.com/watch?v=jE-SpRI3K5g.
#   Design and functionality improved by Henry Graves.

import os
import tkinter as tk
import tkinter.font as TkFont
from tkinter import *
from tkinter import filedialog, simpledialog, Text
from pathlib import Path
from functools import partial

# Bottom button commands
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

    currentProfile = apps[0].removeprefix('appOpener_')
    currentProfile = currentProfile.removesuffix('.txt')
    profileLabel = tk.Label(frame, text=currentProfile + "\n--------------------------------------------------", font=font)
    profileLabel.pack(fill=BOTH)

    for app in appsNoFilepath:
        label = tk.Label(frame, text=app, font=font)
        label.pack(fill=BOTH)

def clearApps():
    answer = tk.messagebox.askyesno(title="Clear Apps", message="Clear current apps?")

    if answer:
        for widget in frame.winfo_children():
            widget.destroy()

        keepProfileName = apps.pop(0)
        apps.clear()
        apps.append(keepProfileName)
        appsNoFilepath.clear()

        currentProfile = apps[0].removeprefix('appOpener_')
        currentProfile = currentProfile.removesuffix('.txt')
        profileLabel = tk.Label(frame, text=currentProfile + "\n--------------------------------------------------", font=font)
        profileLabel.pack(fill=BOTH)

    else:
        tk.messagebox.showinfo(title=None, message="Apps not cleared.")

def runApps():
    for app in apps:
        if (app != apps[0]):
            os.startfile(app)

    root.destroy() # Close App Opener upon running selected apps

# Menubar commands
def changeProfile(inputProfile):
    print("Changing profile...")

    # Saves current list to the appropriate profile.txt (filename is 1st index)
    if (len(apps) > 0):
        oldProfile = apps[0]
        with open(oldProfile, 'w') as file:
            print("Saving previous profile:")
            for app in apps:
                print(app)
                file.write(app + ',')

    # Reads chosen profile and gets its app list.
    # Overwrites appOpener_current.txt with the chosen profile name & apps.
    print(inputProfile)
    if os.path.isfile(inputProfile):
        print("opening profile: " + inputProfile)
        with open(inputProfile, 'r') as file:
            tempApps = file.read()
            newApps = tempApps.split(',')
            newApps = [i for i in newApps if i.strip()] # Gets rid of empty lines
        apps.clear()
        for i in range(0, len(newApps)):
            apps.append(newApps[i])

        with open('appOpener_current.txt', 'w') as file:
            print("overwriting CURRENT")
            for app in newApps:
                print(app)
                file.write(app + ',')

    for widget in frame.winfo_children():
        widget.destroy()

    appsNoFilepath.clear()

    # Create simplified app list
    for i in range(1, len(newApps)):
        p = Path(newApps[i])
        name = p.name.capitalize()
        name = name.removesuffix('.exe')
        appsNoFilepath.append(name)

    # Display the current profile name and app list
    if (len(apps) > 0):
        currentProfile = inputProfile.removeprefix('appOpener_')
        currentProfile = currentProfile.removesuffix('.txt')
        profileLabel = tk.Label(frame, text=currentProfile + "\n--------------------------------------------------", font=font)
        profileLabel.pack(fill=BOTH)

    for app in appsNoFilepath:
        label = tk.Label(frame, text=app, font=font)
        label.pack(fill=BOTH)

def newProfile():
    print("Adding new profile...")

    # Get new profile name through custom messagebox, pass arguments to helper function
    top = Toplevel()
    top.title('Add Profile')
    top.geometry("%dx%d+%d+%d" % (200, 115, 478+314+225, 410))
    Label(top, font=font, text='New profile name:').place(x=10,y=10)
    nameInput = Entry(top, font=font, bd=1, relief="groove")
    nameInput.place(x=10, y=40)
    nameInput.focus()
    Button(top, font=font, text="Save  ", width=6, padx=1, pady=2, bd=1, relief="groove",
        fg="#ffffff", bg="#55acee", command=partial(newProfileHelper, nameInput, top)).place(x=10, y=70)
    Button(top, font=font, text="Cancel", width=6, padx=1, pady=2, bd=1, relief="groove",
        fg="#ffffff", bg="#55acee", command=top.destroy).place(x=70, y=70)

def newProfileHelper(nameInput, top):
    newFileName = "appOpener_" + nameInput.get() + ".txt"
    print("nameInput= "+ newFileName)
    # Create file, add filename to it, add profile filename to master list
    f = open(newFileName, 'w')
    f.write(newFileName+",")
    f.close()
    profiles.append(newFileName)
    if os.path.isfile('appOpener_profileList.txt'):
            print("updating profileList")
            with open('appOpener_profileList.txt', 'w') as file:
                for profile in profiles:
                    file.write(profile + ',')
    # Close the new profile creator window
    top.destroy()

    # Save previous profile
    if (len(apps) > 0):
        oldProfile = apps[0]
        with open(oldProfile, 'w') as file:
            print("Saving previous profile:")
            for app in apps:
                print(app)
                file.write(app + ',')

    # Clear displayed lists
    apps.clear()
    appsNoFilepath.clear()
    for widget in frame.winfo_children():
        widget.destroy()


    # Display the current profile name and app list
    apps.append(newFileName)
    if (len(apps) > 0):
        currentProfile = newFileName.removeprefix('appOpener_')
        currentProfile = currentProfile.removesuffix('.txt')
        profileLabel = tk.Label(frame, text=currentProfile + "\n--------------------------------------------------", font=font)
        profileLabel.pack(fill=BOTH)
    for app in appsNoFilepath:
        label = tk.Label(frame, text=app, font=font)
        label.pack(fill=BOTH)

    # Update profiles in menubar
    profileChangeList.delete(0,len(profiles)+1)
    profileDeleteList.delete(0,len(profiles)+1)
    for profile in profiles:
        print("populate menubar with: " + profile)
        profileChangeList.add_command(label=profile.removeprefix('appOpener_').removesuffix('.txt'), command=partial(changeProfile, profile))
        profileDeleteList.add_command(label=profile.removeprefix('appOpener_').removesuffix('.txt'), command=partial(deleteProfile, profile))

    # Ensure that addAppButton is updated away from "Make a Profile"
    addAppButton['text'] = 'Add App'
    addAppButton['command'] = addApp

def deleteProfile(profile):
    answer = tk.messagebox.askyesno(title="Delete Profile", message="Delete profile '" + profile.removeprefix('appOpener_').removesuffix('.txt') + "'?")
    print("deleting profile: " + profile)

    if answer:
        for widget in frame.winfo_children():
            widget.destroy()
        apps.clear()

        # Delete file
        if "appOpener_" in profile: # Added as a little bit of security / peace of mind while I'm testing this program
            if os.path.exists(profile):
                os.remove(profile)
                print("File deleted")

        profiles.remove(profile)

        if os.path.isfile('appOpener_profileList.txt'):
            print("updating profileList")
            with open('appOpener_profileList.txt', 'w') as file:
                for profile in profiles:
                    file.write(profile + ',')

        # Update profiles in menubar
        profileChangeList.delete(0,len(profiles)+1)
        profileDeleteList.delete(0,len(profiles)+1)
        for profile in profiles:
            print("update profiles in menubar with: " + profile)
            profileChangeList.add_command(label=profile.removeprefix('appOpener_').removesuffix('.txt'), command=partial(changeProfile, profile))
            profileDeleteList.add_command(label=profile.removeprefix('appOpener_').removesuffix('.txt'), command=partial(deleteProfile, profile))

    # Update addAppButton to "Make a Profile" if deleted last profile
    if len(profiles) == 0:
        addAppButton['text'] = 'Make a Profile'
        addAppButton['command'] = newProfile

# Declare and initialize
#########################################################################################################################################
root = tk.Tk()
root.resizable(0, 0)
root.geometry("+1000+400") # Starting position of App Opener - placed near messagebox
root.title('App Opener')
#root.iconbitmap(r'C:\Users\henry\Downloads\171127-200.ico')  # Un-comment this to enable logo
apps = []
appsNoFilepath = []
profiles = []
runAppsList = []
font = TkFont.Font(family="Arial", size=10, weight="bold")
menuFont = TkFont.Font(family="Arial", size=10)
menubar = Menu(root)

# Read saved data
#########################################################################################################################################
# Reads our previous save of apps, converts to array
if os.path.isfile('appOpener_current.txt'):
    with open('appOpener_current.txt', 'r') as file:
        tempApps = file.read()
        apps = tempApps.split(',')
        apps = [i for i in apps if i.strip()] # Gets rid of empty lines

    if (len(apps) > 0):
        currentProfile = apps[0].removeprefix('appOpener_')
        currentProfile = currentProfile.removesuffix('.txt')
else:
    # Make appOpener_current.txt
    f = open("appOpener_current.txt", 'w')
    f.close()

# If also not in existence, make appOpener_profileList.txt
if not os.path.isfile('appOpener_profileList.txt'):
    # Make appOpener_profileList.txt
    f = open("appOpener_profileList.txt", 'w')
    f.close()

# Makes an array of all existing profile names
with open('appOpener_profileList.txt', 'r') as file:
    tempProfiles = file.read()
    profiles = tempProfiles.split(',')
    profiles = [i for i in profiles if i.strip()] # Gets rid of empty lines
print("Profiles available:")
for profile in profiles:
    print(profile)

# Draw UI and display app list
#########################################################################################################################################
# Draw main canvas and frame
canvas = tk.Canvas(root, height=478, width=314, bg="#ffffff")
canvas.pack(fill=BOTH, expand=TRUE)
frame = tk.Frame(root, bg="#ffffff")
frame.place(relwidth=0.8, relheight=0.6, relx=0.1, rely=0.1)

# Buttons
runAppsButton = tk.Button(root, text="Run Apps", font=font, width=10, padx=10, pady=5, bd=1, relief="groove",
    fg="#ffffff", bg="#55acee", command=runApps)
runAppsButton.pack(side="right", fill=Y)

# If no profiles exist, display "Make a Profile" instead of "Add App"
if len(profiles) != 0:
    addAppButton = tk.Button(root, text="Add App", font=font, width=10, padx=10, pady=5, bd=1, relief="groove",
        fg="#ffffff", bg="#55acee", command=addApp)
    addAppButton.pack(side="right", fill=Y)
else:
    addAppButton = tk.Button(root, text="Make a Profile", font=font, width=10, padx=10, pady=5, bd=1, relief="groove",
        fg="#ffffff", bg="#55acee", command=newProfile)
    addAppButton.pack(side="right", fill=Y)

clearAppsButton = tk.Button(root, text="Clear Apps", font=font, width=10, padx=10, pady=5,bd=1, relief="groove",
    fg="#ffffff", bg="#55acee", activebackground="red", command=clearApps)
clearAppsButton.pack(side="right", fill=Y)

# Profiles menu in top menu bar
profileMenu = Menu(menubar, activebackground="#55acee", font=menuFont, relief="groove", tearoff=0)
profileChangeList = Menu(menubar, activebackground="#55acee", font=menuFont, relief="groove", tearoff=0)
profileDeleteList = Menu(menubar, activebackground="#55acee", font=menuFont, relief="groove", tearoff=0)
menubar.add_cascade(label='Profile', menu=profileMenu)
profileMenu.add_cascade(label='Change Profile', menu=profileChangeList)

for profile in profiles:
    profileChangeList.add_command(label=profile.removeprefix('appOpener_').removesuffix('.txt'), command=partial(changeProfile, profile))

profileMenu.add_separator()
profileMenu.add_command(label='New Profile', command=newProfile)
profileMenu.add_cascade(label='Delete Profile', menu=profileDeleteList)

for profile in profiles:
    profileDeleteList.add_command(label=profile.removeprefix('appOpener_').removesuffix('.txt'), command=partial(deleteProfile, profile))

root.config(menu=menubar)

# Create simplified app list
for i in range(1, len(apps)):
    p = Path(apps[i])
    name = p.name.capitalize()
    name = name.removesuffix('.exe')
    appsNoFilepath.append(name)

# Display the current profile name and app list
if (len(apps) > 0):
    profileLabel = tk.Label(frame, text=currentProfile + "\n--------------------------------------------------", font=font)
    profileLabel.pack(fill=BOTH)

for app in appsNoFilepath:
    label = tk.Label(frame, text=app, font=font)
    label.pack(fill=BOTH)

root.mainloop()

# Save apps list
#########################################################################################################################################
# Save file of current apps upon closing
with open('appOpener_current.txt', 'w') as file:
    print("CLOSING - apps saving to current:")
    for app in apps:
        print(app)
        file.write(app + ',')

# Saves current list to the appropriate profile.txt (filename is 1st index)
if (len(apps) > 0):
    oldProfile = apps[0]
    with open(oldProfile, 'w') as file:
       print("CLOSING - apps saving to " + oldProfile + ":")
       for app in apps:
            print(app)
            file.write(app + ',')