#!/usr/bin/python

'''
################################################################################

COPYRIGHT (c) 2017 Marriott Library IT Services.  All Rights Reserved.

Author:          Topher Nadauld - mlib-its-mac-github@lists.utah.edu
Creation Date:   December 14, 2016
Last Updated:    Auguest 9, 2017

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted, provided that
the above copyright notice appears in all copies and that both that copyright
notice and this permission notice appear in supporting documentation, and that
the name of The Marriott Library not be used in advertising or publicity
pertaining to distribution of the software without specific, written prior
permission. This software is supplied as-is without expressed or implied
warranties of any kind.


################################################################################
'''


import os
import socket
import subprocess
import sys
import re
import time
import urllib2
import webbrowser

## Jamf Pro specified defaults from the Jamf Pro installer guide.
mysql_user = "root"
mysql_database_name = "jamfsoftware"
mysql_database_username = "jamfsoftware"
mysql_database_password = "jamfsw03"
mysql_database_hostname = "localhost"

Jamf_file_location = "/Library/JSS/"
tomcat_location = Jamf_file_location + "Tomcat/"
Jamf_webapp_location = Jamf_file_location + "ROOT.war"

def mysql_command(action, mysql_password):
    
    ## This function takes in a MySQL command and preforms it without having to go to interactive mode.
    
    try:
        subprocess.call (["/usr/local/mysql/bin/mysql", "-h", mysql_database_hostname, "-u", mysql_user, "-p" + mysql_password, "--connect-expired-password", "-e", action])
        print action + "... was Successfull!"
    except:
        print action + "... had a problem finishishing successfully."

def change_sql_password():

    ## This function recreates the root password for the MySQL database. 
    
    print "Changing the MySQL password"
    
    # Stop the MySQL Server
    try:
        subprocess.call(["launchctl", "unload", "-F", "/Library/LaunchDaemons/com.oracle.oss.mysql.mysqld.plist"])
        print "Sucessfully stopped the MySQL server"
    except:
        print "The server was already stopped or there was a error stopped the server."
    
    # Find the data folder and delete it.
    if os.path.exists('/usr/local/mysql/data/mysql/db.frm'):
        try:
            subprocess.call (["rm", "-R", "/usr/local/mysql/data"])
        except:
            print "There was a problem deleting the MySQL data folder"
    else:
        print "The MySQL data folder was not found"
    
    # Rebuild the data folder and get the password.
    try:
        password_output = subprocess.check_output(["sudo", "/usr/local/mysql/bin/mysqld", "--no-defaults", "--initialize", "--basedir=/usr/local/mysql", "--datadir=/usr/local/mysql/data", "--user=mysql", "--tmpdir=/var/tmp"], stderr=subprocess.STDOUT)
    except:
        print "There was a problem recreating the data folder....Password was not reset."
    
    password = re.findall("localhost: (.*)", password_output)[0]
    
    print "The temp password is: " + password
    
    # Start the MySQL server.
    try:
        subprocess.call(["launchctl", "load", "-F", "/Library/LaunchDaemons/com.oracle.oss.mysql.mysqld.plist"])
    except:
        print 'Mysql did not startup'
    
    time.sleep(2)

    # Change the MySQL password to the Jamf Pro specified defaults.
    mysql_command("ALTER USER " + mysql_user + "@" + mysql_database_hostname + " IDENTIFIED BY " + "'" + mysql_database_password + "'" + ";", password)
    
    print "The MySQL password has been changed."

def configure_sql_for_jamf_pro():
    
    ## Create a MySQL database and grant permissions using Jamf Pro specified defaults.
    print "Configuring the MySQL service"
    mysql_command("create database " + mysql_database_name + ";", mysql_database_password)
    mysql_command("GRANT ALL ON " + mysql_database_name + " .* TO " + mysql_database_username + "@" + mysql_database_hostname + " IDENTIFIED BY " + "'" + mysql_database_password + "'" + ";", mysql_database_password)

    print "The MySQL Database has been created."

def install_tomcat():

    # Install tomcat
    print "Installing Tomcat"
    
    tomcat_url = "http://tomcat.apache.org/download-80.cgi"
    req = urllib2.Request(tomcat_url)
    page_source = urllib2.urlopen(req)
    for x in page_source:
        #print(x)
        if '<h3 id=' in x:
            if "8.0" in x:
                print "Found Version"
                tomcat_version = x.split(">")[1]
                tomcat_version = tomcat_version.split("<")[0]
                print tomcat_version
    
    path="http://www.apache.org/dist/tomcat/tomcat-8/v" + tomcat_version + "bin/apache-tomcat-" + tomcat_version + ".tar.gz"
    
def configure_tomcat():

    ## This function configures Tomcat to have the correct keystore for the computer, 
    ## builds the log folder and starts Tomcat.
    
    if os.path.exists(tomcat_location + "logs"):
       print "The logs directory for Tomcat have already been created"
    else:
        try:
            subprocess.call(["/bin/mkdir", tomcat_location + "logs"])
            print "The logs directory for Tomcat has sucessfully been created"
        except:
            print "There was a problem creating the logs directory for tomcat."
    
    try:
        subprocess.call(["/usr/bin/keytool", "-genkey", "-alias", "tomcat", "-keyalg", "RSA", "-keypass", "changeit", "-storepass", "changeit", "-dname", "CN=Self Signed, OU=JAMFSW, O=JAMF Software, L=Minneapolis, ST=MN, C=US", "-keystore", tomcat_location + ".keystore"])
        print "The keystore has been created sucessfully."    
    except:
        print "The Keystore was not generated."
        
    try:
        subprocess.call([Jamf_file_location + "tomcat/bin/startup.sh"])
        print "Tomcat has been started"
    except:
        print "Tomcat was not started."
    
def main():
    
    ## This script creates a new Jamf Pro instance on a virtual machine.
    
    ## Configure MySQL
    change_sql_password()
    configure_sql_for_jamf_pro()
    
    ## Configure Tomcat
    #install_tomcat() # This is installed using the Jamf Pro installer with AutoDMG.
    configure_tomcat()

    ## Wait and launch safari.
    print "Waiting for the Jamf Pro instance to start before starting Safari"
    time.sleep(30)
    
    try:
        subprocess.call(['launchctl', 'load', '/Library/LaunchAgents/edu.utah.scl.start_safari.plist'])
    except:
        print "There was a problem with the starting safari script."
  
    ## Stops the configure script from running each time a user logs in.
    ## The loginwindow.plist contains a loginhook the runs the configure script.
    try:
        subprocess.call(["rm", "/var/root/Library/Preferences/com.apple.loginwindow.plist"])
    except:
        print "The loginwindow.plist was not deleted. Computer will run the script on next login."

if __name__ == '__main__':
    main()
