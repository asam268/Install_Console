#!/usr/bin/env python

"""Install Console GUI

:author: Asa Marshall

This program provides a user interface to name a computer, provide an asset tag, install Ivanti LANDesk, add the
computer to the GCSU domain, install Munki Tools, and run managed software updates. This program works in tandem with
4 other scripts:

Validate:           Confirms that the password entered for this program is valid for a root user
LandeskAgent2016:   Installs Ivanti LANDesk
AssetTag:           Writes Asset Tag to the appropriate preference file for LANDesk management
Network:            Adds the computer to the GCSU domain
"""

import Tkinter as tk
from Tkinter import *
import tkMessageBox
import ttk
import os
import subprocess
import Munki_Tools

# Global Variables
computer_name = ""  # Value for the name of the current system
asset_tag = ""  # Value for the asset tag of the current system
root = tk.Tk()  # Root function for GUI
msg_repo = Entry(root)  # Entry for software repo URL
msg_manifest = Entry(root)  # Entry for server manifest
var_ivanti = IntVar()  # Holds 'is checked' value for Ivanti check box
var_atag = IntVar()  # Holds 'is checked' value for Asset Tag check box
var_network = IntVar()  # Holds 'is checked' value for Network check box
var_munki = IntVar()  # Holds 'is checked' value for software install check box
attempts = 0  # Number of attempts when enter password


def get_computer_name():
    """Gets the current name of the computer

    :return: str, computer name
    """

    output = os.popen("scutil --get ComputerName").read()
    return output


def get_asset_tag():
    """Gets the current asset tag of the computer

    :return: str, asset tag
    """

    output = os.popen("defaults read /Library/Preferences/com.apple.RemoteDesktop.plist Text1").read()
    return output


def get_repo():
    """Gets the currently configured software repo URL for Munki

    :return: str, software repo URL
    """

    output = os.popen("defaults read /Library/Preferences/ManagedInstalls.plist SoftwareRepoURL").read()
    return output


def get_manifest():
    """Gets the currently configured server manifest/client identifier

    :return: str, manifest name
    """

    output = os.popen("defaults read /Library/Preferences/ManagedInstalls.plist ClientIdentifier").read()
    return output


# TODO: Change the color of the okay button
def pwd_window(c, a):
    """Password window that retrieves admin password to execute commands based on data entered in the main GUI.

    :param c: Tkinter Entry, computer name
    :param a: Tkinter Entry, asset tag
    :return:
    """

    global computer_name
    global asset_tag
    global attempts
    attempts = 0
    computer_name = c.get()
    asset_tag = a.get()

    pop = tk.Toplevel(bg="#ECECEC")
    pop.wm_title("Enter Password")
    pop_frame = Frame(pop, bg="#ECECEC")

    label = ttk.Label(pop_frame, text="Password:", font=NORMAL)
    pwd = ttk.Entry(pop_frame, show='*')
    b1 = ttk.Button(pop_frame, text='Okay', command=lambda: exec_changes(pwd, pop))
    b2 = ttk.Button(pop_frame, text='Cancel', command=lambda: pop.destroy())

    pop_frame.pack()
    label.pack(side='top', fill='x', padx=10)
    pwd.pack(fill='x', padx=10)
    b1.pack(side='right')
    b2.pack(side='left')

    pop.mainloop()


def validate(pwd):
    """Validates admin password.

    The method runs a script with the password given. If the script is run with root privileges, it will echo 'True.'


    :param pwd: str, admin password
    :return: True only if the admin password is correct
    """

    os.chdir(sys.path[0])
    cmd = "./Resources/Validate"
    exec_cmd = "echo %s|sudo -S %s" % (pwd, cmd)
    os.system("echo %s|sudo -S -v" % pwd)
    try:
        result = subprocess.check_output(exec_cmd, shell=True)
        if result.startswith('T'):
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False


# TODO: Activate functions when implementing
def exec_changes(e, pop):
    """Executes functions based off the data entered in the main GUI.

    :param e: Tkinter entry, stores admin password
    :param pop: Tkinter frame
    :return: void
    """

    global attempts
    pwd = e.get()
    pwd = "'" + pwd + "'"

    if validate(pwd):
        # set_computer_name(pwd)
        set_asset_tag(pwd)
        if var_ivanti.get():
            # run_ivanti_script(pwd)
            print("Ivant checked")
        if var_atag.get():
            # run_asset_tag_script(pwd)
            print("Asset tag checked")
        if var_network.get():
            # run_network_script(pwd)
            print("Network checked")
        if var_munki.get():
            set_repo(pwd)
            set_manifest(pwd)
            Munki_Tools.managed_software_update(pwd)
            print("Munki checked")
        # enable_fast_user_switching(pwd)
        os.system("sudo -k")
        pop.destroy()
        root.destroy()
    else:
        attempts += 1
        if attempts <= 1:
            lblerror = ttk.Label(pop, text="Password Incorrect.", font=NORMAL)
            lblerror.pack()


def set_computer_name(pwd):
    """Sets the name of the computer from the data entered in the main GUI.

    The method sets the name on 3 different scutil variables: ComputerName, HostName, and LocalHostName. Setting these
    three are essential for Ivanti management.

    :param pwd: str, admin password
    :return: void
    """

    global computer_name
    computer_name = "\"" + computer_name + "\""
    cmd = "scutil --set ComputerName " + computer_name
    os.system("echo %s|sudo -S %s" % (pwd, cmd))
    cmd = "scutil --set HostName " + computer_name
    os.system("echo %s|sudo -S %s" % (pwd, cmd))
    cmd = "scutil --set LocalHostName " + computer_name
    os.system("echo %s|sudo -S %s" % (pwd, cmd))


def set_asset_tag(pwd):
    """Sets the Asset Tag based of data entered in the main GUI.

    :param pwd: str, admin password
    :return: void
    """

    global asset_tag
    cmd = "defaults write /Library/Preferences/com.apple.RemoteDesktop.plist Text1 " + asset_tag
    os.system("echo %s|sudo -S %s" % (pwd, cmd))


def set_repo(pwd):
    """Sets the software repo URL to the text written in the repo entry.

    :param pwd: str, admin password
    :return: void
    """

    global msg_repo
    repo = msg_repo.get()
    cmd = "defaults write /Library/Preferences/ManagedInstalls.plist SoftwareRepoURL " + repo
    os.system("echo %s|sudo -S %s" % (pwd, cmd))


def set_manifest(pwd):
    """Sets the manifest/client identifier to the text written in the manifest entry.

    :param pwd: str, admin password
    :return: void
    """

    global msg_manifest
    manifest = msg_manifest.get()
    cmd = "defaults write /Library/Preferences/ManagedInstalls.plist ClientIdentifier " + manifest
    os.system("echo %s|sudo -S %s" % (pwd, cmd))


# TODO: Needs testing for dmg removal
def run_ivanti_script(pwd):
    """Runs script to install Ivanti LANDesk if Ivanti checkbox is checked on the main GUI

    :param pwd: str, admin password
    :return:
    """

    cmd = "./Resources/LandeskAgent2016"
    os.system("echo %s|sudo -S %s" % (pwd, cmd))
    # if os.path.exists("./LandeskAgent2016.dmg"):
    #     os.system("rm ./LandeskAgent2016.dmg")


def run_asset_tag_script(pwd):
    """Runs Perl script for finalizing Asset Tag data

    :param pwd: str, admin password
    :return: void
    """

    cmd = "./Resources/AssetTag"
    os.system("echo %s|sudo -S %s" % (pwd, cmd))


def run_network_script(pwd):
    """Runs script to add computer to the GCSU Network.

    :param pwd: str, admin password
    :return: void
    """

    cmd = "./Resources/Network"
    os.system("echo %s|sudo -S %s" % (pwd, cmd))


def enable_fast_user_switching(pwd):
    """Enables settings for fast user switching at login window

    :param pwd: str, admin password
    :return: void
    """

    cmd = "defaults write /Library/Preferences/com.apple.loginwindow SHOWFULLNAME -bool true"
    os.system("echo %s|sudo -S %s" % (pwd, cmd))
    cmd = "defaults write /Library/Preferences/.GlobalPreferences MultipleSessionEnabled -bool YES"
    os.system("echo %s|sudo -S %s" % (pwd, cmd))


def ivanti_warning():
    """Displays a message box warning.

    The message box is displayed when the Ivanti checkbox is unchecked.

    :return: void
    """

    if not var_ivanti.get():
        tkMessageBox.showwarning("Ivanti LANDesk Warning", "The Asset Tag script will only work if LANDesk is "
                                                           "installed.")


def munki_console(frame_m):
    """Creates GUI for Munki Functionality.

    If Munki is installed, the GUI shows entries for the repo URL and manifest, including a checkbox for choosing on
    whether to run a managed software update or not.

    If Munki is not installed, the method only displays a button that installs Munki Tools.

    :param frame_m: Tkinter frame
    :return: void
    """

    global msg_repo
    global msg_manifest
    if os.path.exists("/Library/Preferences/ManagedInstalls.plist"):
        repo = get_repo()
        manifest = get_manifest()
        lbl_munki = Label(frame_m, text="Munki Configuration", pady=7, relief=RAISED, bg="#ECECEC")
        lbl_repo = Label(frame_m, text="Software Repo URL", bg="#ECECEC")
        lbl_manifest = Label(frame_m, text="Manifest (Client Identifier)", bg="#ECECEC")
        msg_repo = ttk.Entry(frame_m)
        msg_repo.insert(0, repo)
        msg_manifest = ttk.Entry(frame_m)
        msg_manifest.insert(0, manifest)
        cb_munki = Checkbutton(frame_m, text="Run Software Installation", variable=var_munki, bg="#ECECEC")

        lbl_munki.pack()
        lbl_repo.pack()
        msg_repo.pack()
        lbl_manifest.pack()
        msg_manifest.pack()
        cb_munki.pack()
    else:
        installer = ttk.Button(frame_m, text="Install Munki", command=lambda: install_munki_tools())
        installer.pack()


def install_munki_tools():
    """Calls functions to install Munki Tools.

    The method first shows a warning stating that the Munki Tools requires a reboot after installation.

    After the warning, the method calls a password window from Munki_Tools.py.

    :return: void
    """

    tkMessageBox.showwarning("Install Munki Tools", "Installing Munki Tools will require a system reboot.")
    Munki_Tools.munki_pwd()


def initialize():
    """Sets up the main GUI for the program.

    :return: void
    """

    root.title("Install Console")
    root.configure(bg="#ECECEC")
    frame = tk.Frame(root, bg="#ECECEC")
    frame_m = tk.Frame(root, bg="#ECECEC")
    # gets current computer name and Asset tag to populate message boxes
    cname = get_computer_name()
    atag = get_asset_tag()

    # labels and entries
    lbl_remote = Label(frame, text="Please activate all privileges for\nRemote Management in Sharing\nSettings before "
                                   "using this program.", relief=RAISED, bg="#ECECEC")
    lbl_cname = Label(frame, text="Computer Name", bg="#ECECEC")
    msg_cname = ttk.Entry(frame)
    msg_cname.insert(0, cname)

    lbl_atag = Label(frame, text="Asset Tag", bg="#ECECEC")
    msg_atag = ttk.Entry(frame)
    msg_atag.insert(0, atag)

    # check buttons: checked by default since all scripts should be run with fresh computers
    cb_ivanti = Checkbutton(frame, text="Run Ivanti Script", variable=var_ivanti, bg="#ECECEC",
                            command=lambda: ivanti_warning())
    cb_ivanti.select()
    cb_atag_script = Checkbutton(frame, text="Run Asset Tag Script", variable=var_atag, bg="#ECECEC")
    cb_atag_script.select()
    cb_network = Checkbutton(frame, text="Run Network Script", variable=var_network, bg="#ECECEC")
    cb_network.select()

    # Execute button: opens password window
    btn_cname = ttk.Button(frame_m, text="Execute", command=lambda: pwd_window(msg_cname, msg_atag))

    # populate GUI
    lbl_remote.pack()
    lbl_cname.pack()
    msg_cname.pack()
    lbl_atag.pack()
    msg_atag.pack()
    cb_ivanti.pack()
    cb_atag_script.pack()
    cb_network.pack()
    munki_console(frame_m)
    frame.pack()
    frame_m.pack()
    btn_cname.pack()

    # drive GUI
    root.mainloop()
