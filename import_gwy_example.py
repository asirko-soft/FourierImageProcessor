#! d:\python2\python.exe
# -*- coding: utf-8 -*-
"""
1) install python 2.7 32-bit
2) set HKEY_CURRENT_USER\SOFTWARE\Python\PythonCore\2.7\InstallPath : 
    (Default) = path to python dir
    ExecutablePath = path to python.exe
    WindowedExecutablePath = path to pythonw.exe
3) install packages pygtk, pycario and pygobject 
    https://sourceforge.net/projects/gwyddion/files/pygtk-win32/
4) install gwyddion 32-bit version """
import FindGwyddion as FG
import os
import sys
#sys.path.append('/the/path/to/the/gwyutils/module')
#sys.path.append("D:/Program Files (x86)/Gwyddion/bin")


FG.SEARCH_FOR="gwyddion.exe"
FG.PATH_HINT="C:\\" # Or whatever disk you use
GWYDDION_PATH=FG.find()

if (GWYDDION_PATH is not None):
    print ">>> Appending to 'sys.path'"
    sys.path.append(GWYDDION_PATH)
    print ">>> Importing MODULE 'gwy'"
    import gwy
    
else:
    sys.exit(">>> Gwyddion NOT found!")


