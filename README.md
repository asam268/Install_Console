# Install_Console
Imaging software for GCSU Mac Systems

This program provides a user interface to name a computer, provide an asset tag, install Ivanti LANDesk, add the computer to the GCSU domain, install Munki Tools, and run managed software updates. This program works in tandem with 4 other scripts:

```
Validate: Confirms that the password entered for this program is valid for a root user
LanDeskAgent2016: Installs Ivanti LANDesk 
AssetTag: Writes Asset Tag to the appropriate preference file for LANDesk management
Network: Adds the computer to the GCSU domain
```


## Getting Started
How to get this software running correctly.

### Prerequisites
Among other functions, this software sets up Mac systems for Ivanti remote management. Unfortunately, since this no longer can be done through script, the appropriate preferences must be set for this program to work.

1. Navigate to Sharing Settings (System Preferences > Sharing).
2. In the Service menu on the left, check Remote Management.
3. After checking this option, a menu appears with the prompt, "All local users can access this computer to: ". Check all options on this menu. (If this menu does not appear, select "Options..." in the bottom right of the window).
4. With Remote Management selected in the Service menu, select "Computer Settings..." on the right of the window.
5. (Optional) Enter the device's asset tag in the "Info 1" textbox under "Computer Information."
6. Close System Preferences.

This software only works if the user has access to root/admin privileges.

### Installing
The program is contained inside a folder called, "Install_Console". Simply drag this folder to your desktop.


## Deployment
Inside the "Install_Console" folder, there is an executable file called "Install_Console", two python files, and two 
directories. Selecting "Install_Console" will launch the program.

The main menu that appears upon launching the program may vary if Munki Tools is installed.

### Deployment without Munki Tools
If you plan on using Munki to push a managed software installation to your device, it is highly recommended to select 
the button "Install Munki" before continuing.

There are two text boxes for setting the computer name as well as the asset tag. If you performed the optional step 5 in
the Prerequisites, the asset tag should appear in its respective text box. Note: even if you did not enter the asset tag
in the optional step, you still have to select "Computer Settings..." in the Sharing Menu for this program to work
correctly.

The three checkboxes enable scripts upon executing the program. The issues known with the scripts is that the asset tag
script will not work if LANDesk is not installed.

Clicking the "Execute" button will present a password window.

### Deployment with Munki Tools
With Munki Tools installed, the program has the same functionality as mentioned above. Instead of displaying an 
"Install Munki" button, an extended menu appears providing options for specifying a software repo URL, a server 
manifest/client identifier, and a checkbox for running a software installation.


## Built With
* Python 2.7 - Central scripting framework
* Tkinter - GUI

## Author
Asa Marshall




