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

Navigate to Sharing Settings
```
System Preferences > Sharing
```


