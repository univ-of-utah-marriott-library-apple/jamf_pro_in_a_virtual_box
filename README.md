# Jamf Pro in a Virtual Box
Jamf Pro server can be a funny and fickle beast. When testing different policies that are unique or upgrading to a new version of Jamf Pro, it's best not to try it on the production server first. Sometimes the process of testing a new release or beta can easily break, and having an automated process to quickly rebuild a macOS test environment can save you tons of time and frustration. These instructions are built using macOS but the methodology might be able to be applied to other Operating Systems. 
## Contents

* [Download](#download) - Get the configuration scripts
* [Contact](#contact) - How to reach us
* [Purpose](#purpose) - What is this script for?
* [Usage](#usage) - Details of invocation
  * [Configure_Jamf_Pro.py](#Configure_Jamf_Pro.py)
  * [Start_Safari.py](#Start_Safari.py)
  * [Apple Setup Done](#apple-setup-done)

## Download

[Download the latest version of scripts to create a development Jamf Pro server here!](../../releases/)


## Contact

If you have any comments, questions, or other input, either [file an issue](../../issues) or [send an email to us](mailto:mlib-its-mac-github@lists.utah.edu). Thanks!

## Purpose
Jamf Pro server can be a funny and fickle beast. When testing different policies that are unique or upgrading to a new version of Jamf Pro, it's best not to try it on the production server first. Sometimes the process of testing a new release or beta can easily break, and having an automated process to quickly rebuild a macOS test environment can save you tons of time and frustration. These instructions are built using macOS but the methodology might be able to be applied to other Operating Systems.

## Usage
In the process of creating a development Jamf Pro server, we need to configure the server while the virtual machine is booting up. Using the `Configure Jamf Pro` script, it will configure `MySQL` and start `Tomcat` to the specificed settings. When the configuration is complete and the computer is logged in, the `Start Safari` script will launch the webpage to finish configuring the Jamf Pro server. The `Apple Setup Done` is a trigger to prevent the Apple Setup dialog boxes from displaying.

### Configure_Jamf_Pro.py
`Configure_Jamf_Pro.py` is a Python script to mimic the Jamf Pro installer process but without all the prompts. The script will configure and start both `MySQL` and `Tomcat`. To configure`MySQL`, I needed to know what the admin password was without prompt the user. I found that when I removed `/usr/local/mysql/data/mysql/db.frm` and ran the initialize command again, `MySQL` would create a new password and return it. With the password in hand I can set the root password for `MySQL` and configure the database to the specifications of Jamf Pro. For `Tomcat`, I had to create the self signing certificate that the computer uses to authenticate to the Jamf Pro server. `Tomcat` also needed some specific logging directories before it would start.

### Start_Safari.py
`Start_Safari.py` is a Python script and a launchagent. The launchagent is loaded when the `Configure_Jamf_Pro.py` script finishes. Once the user is completely login the script launches Safari and opens the webpage to setup Jamf Pro. 

### Apple Setup Done
`Apple Setup Done` is a package that contains the trigger file to prevent the Apple Setup dialog boxes from displaying when starting up the computer for the first time. To build the package from scratch follow the instructions on the blog.

For detailed instructions on building a development Jamf Pro server, check out:  [Jamf Pro in a Virtual Box](https://apple.lib.utah.edu/jamf-pro-in-a-virtual-box/)

## Update History

| Date       | Version | Notes            |
| ---------- | ------- | ---------------- |
| 2017.08.23 | 1.0.0   | Initial version. |
