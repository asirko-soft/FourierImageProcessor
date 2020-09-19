#FindGwyddion.py

import os

SEARCH_FOR=""
PATH_HINT=""

def find():

    print ">>> Searching for '" + SEARCH_FOR + "' on '" + PATH_HINT + "'"

    for root, dirs, files in os.walk(PATH_HINT):
        for name in files:
            if name == SEARCH_FOR:
                PATH = os.path.abspath(root)
                print ">>> Gwyddion found at: ", PATH
                return PATH
