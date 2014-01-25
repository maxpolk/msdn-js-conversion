#! /usr/bin/env python
'''
Get a fragment of an XML file and pretty print it
'''

import sys
from xml.etree import ElementTree
from xml.dom.minidom import parseString

usage = "Usage: get-fragment.py INPUTFILE ELEMENTID"

# Parse args
if len (sys.argv) != 3:
    raise Exception ("ERROR: Invalid number of arguments\n{:}".format (usage))
inputfile = sys.argv[1]
elementid = sys.argv[2]

# Parse XML file and find element having given id
tree = ElementTree.parse (inputfile)
root = tree.getroot ()
for element in root.findall (".//*[@id='{:}']".format (elementid, elementid)):
    print parseString (ElementTree.tostring (element)).toprettyxml (indent="  ")
