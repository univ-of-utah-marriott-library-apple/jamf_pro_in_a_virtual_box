# Configure Jamf Pro

To create a configure jamf pro package, the scripts need to be placed in specific places.

## Installation  

`configure_jamf_pro.py` and `start_safari.py` need to be placed in `/Library/JSS/`. These are the main scripts that automate the development Jamf Pro Server.

The `edu.utah.scl.start_safari.plist` needs to be placed in `/Library/LaunchAgents/`.  The LaunchAgent loads Safari when the user is fully logged in and ready.

The`com.apple.loginwindow.plist` needs to be placed in `/var/root/Library/Preferences/` The Loginwindow contains a hook to start `configure_jamf_pro.py`. 

