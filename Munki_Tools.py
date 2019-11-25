#!/usr/bin/env/ python

"""Additional functions for Munki

This file contains methods specific to Munki for the Install Console. The file contains a separate method for entering
a password, a way to install Munki, and initializing a managed software update.

"""

import os
import Tkinter as tk
from Tkinter import *
import ttk
import GUI

attempts = 0


def munki_pwd():
    """Password window for installing Munki Tools

    Similar to the main password window, but this one just installs Munki.
    :return: void
    """

    global attempts
    attempts = 0

    pop_m = tk.Toplevel(bg="#ECECEC")
    pop_m.wm_title("Enter Password")
    pop_frame = Frame(pop_m, bg="#ECECEC")

    label = ttk.Label(pop_frame, text="Password:", font=NORMAL)
    pwd = ttk.Entry(pop_frame, show='*')
    b1 = ttk.Button(pop_frame, text='Okay', command=lambda: munki_install(pwd, pop_m))
    b2 = ttk.Button(pop_frame, text='Cancel', command=lambda: pop_m.destroy())

    pop_frame.pack()
    label.pack(side='top', fill='x', padx=10)
    pwd.pack(fill='x', padx=10)
    b1.pack(side='right')
    b2.pack(side='left')


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
            lblerror = ttk.Label(pop_m, text="Password Incorrect.", font=NORMAL)
            lblerror.pack()


def managed_software_update(pwd):
    """Initializes a managed software update using Munki

    :param pwd: str, admin password
    :return: void
    """

    cmd = "echo %s|sudo -S managedsoftwareupdate -vv" % pwd
    os.system(cmd)
    cmd = "echo %s|sudo -S managedsoftwareupdate --installonly -v" % pwd
    os.system(cmd)
