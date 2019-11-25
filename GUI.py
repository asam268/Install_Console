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
msgRepo = Entry(root)  # Entry for software repo URL
msgManifest = Entry(root)  # Entry for server manifest
varIvanti = IntVar()  # Holds 'is checked' value for Ivanti check box
varAtag = IntVar()  # Holds 'is checked' value for Asset Tag check box
varNetwork = IntVar()  # Holds 'is checked' value for Network check box
varMunki = IntVar()  # Holds 'is checked' value for software install check box
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
    # print "" + sys.path[0]
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
        # set_asset_tag(pwd)
        if varIvanti.get():
            # run_ivanti_script(pwd)
            print("Ivant checked")
        if varAtag.get():
            # run_asset_tag_script(pwd)
            print("Asset tag checked")
        if varNetwork.get():
            # run_network_script(pwd)
            print("Network checked")
        if varMunki.get():
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
        # print "Password Incorrect"
        if attempts <= 1:
            lblerror = ttk.Label(pop, text="Password Incorrect.", font=NORMAL)
            lblerror.pack()


# Sets the ComputerName and HostName of the computer from the data entered in the main GUI
# Parameters:   pwd - Admin password
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


# Sets the Asset Tag based of data entered in the main GUI.
def set_asset_tag(pwd):
    """Sets the Asset Tag based of data entered in the main GUI.

    :param pwd: str, admin password
    :return: void
    """

    global asset_tag
    cmd = "defaults write /Library/Preferences/com.apple.RemoteDesktop.plist Text1 " + asset_tag
    os.system("echo %s|sudo -S %s" % (pwd, cmd))
    # print(get_asset_tag())


def set_repo(pwd):
    """Sets the software repo URL to the text written in the repo entry.

    :param pwd: str, admin password
    :return: void
    """

    global msgRepo
    repo = msgRepo.get()
    cmd = "defaults write /Library/Preferences/ManagedInstalls.plist SoftwareRepoURL " + repo
    os.system("echo %s|sudo -S %s" % (pwd, cmd))


def set_manifest(pwd):
    """Sets the manifest/client identifier to the text written in the manifest entry.

    :param pwd: str, admin password
    :return: void
    """

    global msgManifest
    manifest = msgManifest.get()
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

    if not varIvanti.get():
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

    global msgRepo
    global msgManifest
    if os.path.exists("/Library/Preferences/ManagedInstalls.plist"):
        repo = get_repo()
        manifest = get_manifest()
        lblMunki = Label(frame_m, text="Munki Configuration", pady=7, relief=RAISED)
        lblRepo = Label(frame_m, text="Software Repo URL")
        lblManifest = Label(frame_m, text="Manifest (Client Identifier)")
        msgRepo = Entry(frame_m)
        msgRepo.insert(0, repo)
        msgManifest = Entry(frame_m)
        msgManifest.insert(0, manifest)
        cbMunki = Checkbutton(frame_m, text="Run Software Installation", variable=varMunki)

        lblMunki.pack()
        lblRepo.pack()
        msgRepo.pack()
        lblManifest.pack()
        msgManifest.pack()
        cbMunki.pack()
    else:
        installer = Button(frame_m, text="Install Munki", command=lambda: install_munki_tools())
        installer.pack()


def install_munki_tools():
    """Calls functions to install Munki Tools.

    The method first shows a warning stating that the Munki Tools requires a reboot after installation.

    After the warning, the method calls a password window from Munki_Tools.py.

    :return: void
    """

    tkMessageBox.showwarning("Install Munki Tools", "Installing Munki Tools will require a system reboot.")
    # Munki_Tools.test_print()
    Munki_Tools.munki_pwd()


def initialize():
    """Sets up the main GUI for the program.

    :return: void
    """

    root.title("Install Console")
    frame = tk.Frame(root)
    frame_m = tk.Frame(root)
    # gets current computer name and Asset tag to populate message boxes
    cname = get_computer_name()
    atag = get_asset_tag()

    # labels and message boxes
    lblRemote = Label(frame, text="Please activate all privileges for\nRemote Management in Sharing\nSettings before "
                                  "using this program.", relief=RAISED)
    lblCname = Label(frame, text="Computer Name")
    msgCname = Entry(frame)
    msgCname.insert(0, cname)

    lblAtag = Label(frame, text="Asset Tag")
    msgAtag = Entry(frame)
    msgAtag.insert(0, atag)

    # check buttons: checked by default since all scripts should be run with fresh computers
    cbIvanti = Checkbutton(frame, text="Run Ivanti Script", variable=varIvanti, command=lambda: ivanti_warning())
    cbIvanti.select()
    cbAtagScript = Checkbutton(frame, text="Run Asset Tag Script", variable=varAtag)
    cbAtagScript.select()
    cbNetwork = Checkbutton(frame, text="Run Network Script", variable=varNetwork)
    cbNetwork.select()

    # Execute button: opens password window
    btnCname = ttk.Button(frame_m, text="Execute", command=lambda: pwd_window(msgCname, msgAtag))

    # populate GUI
    lblRemote.pack()
    lblCname.pack()
    msgCname.pack()
    lblAtag.pack()
    msgAtag.pack()
    cbIvanti.pack()
    cbAtagScript.pack()
    cbNetwork.pack()
    munki_console(frame_m)
    frame.pack()
    frame_m.pack()
    btnCname.pack()

    # drive GUI
    root.mainloop()
