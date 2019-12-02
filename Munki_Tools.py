#!/usr/bin/env/ python

"""Additional functions for Munki

This file contains methods specific to Munki for the Install Console. The file contains a separate method for entering
a password, a way to install Munki, and initializing a managed software update.

"""

import os
from Tkinter import *
import ttk
import GUI

attempts = 0


def munki_install(e, pop_m):
    """Installs Munki Tools

    Takes a password and opens the Munki Tools .pkg if given the correct password.

    :param e: Entry, password
    :param pop_m: Tkinter Frame
    :return: void
    """

    global attempts
    pwd = e.get()
    pwd = "'" + pwd + "'"
    if GUI.validate(pwd):
        cmd = "echo %s|sudo -S open ./Resources/munkitools.pkg" % pwd
        os.system(cmd)
        pop_m.destroy()
    else:
        attempts += 1
        if attempts <= 1:
            lbl_error = ttk.Label(pop_m, text="Password Incorrect.", font=NORMAL)
            lbl_error.pack()


def managed_software_update(pwd):
    """Initializes a managed software update using Munki

    :param pwd: str, admin password
    :return: void
    """

    cmd = "echo %s|sudo -S managedsoftwareupdate -vv" % pwd
    os.system(cmd)
    cmd = "echo %s|sudo -S managedsoftwareupdate --installonly -v" % pwd
    os.system(cmd)
