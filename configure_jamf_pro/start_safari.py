#!/usr/bin/python

'''
################################################################################

COPYRIGHT (c) 2017 Marriott Library IT Services.  All Rights Reserved.

Author:          Topher Nadauld - mlib-its-mac-github@lists.utah.edu
Creation Date:   December 14, 2016
Last Updated:    Auguest 23, 2017

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


import webbrowser
import subprocess
import time

def main():
    
    # Launch Safari
    subprocess.call(["open", "-a", "/Applications/Safari.app"])
    time.sleep(5)
    
    # Connect to the Jamf Pro website.
    webbrowser.open("https://127.0.0.1:8443")


if __name__ == '__main__':
    main()
