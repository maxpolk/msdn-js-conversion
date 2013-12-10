#! /usr/bin/env python

import os
import sys

def processSection (rewrite, section_name, section):
    '''For given file, process the contents of the named section.'''
    print "Section \"{}\" contains {} lines:".format (section_name, len (section))
    # Determine if we should eliminate this section
    if section_name == "Requirements":
        print "Skipping Requirements section"
    else:
        # Write section header
        if section_name != "":
            rewrite.write ("=={}==\n".format (section_name))
        count = 1
        for line in section:
            print "{} > {}".format (count, line)
            rewrite.write ("{}\n".format (line))
            count += 1

def processFile (filename):
    '''
    Read through a file, separating into mediawiki markup sections.
    Rewrite each section into a new file named with suffix ".rewrite".
    '''
    print ("===== {} =====".format (filename))
    rewrite = open (filename + ".rewrite", 'w')
    section_name = ""
    section = []
    with open (filename) as filein:
        for line in filein:
            line = line.rstrip ("\n")
            if line.startswith ("="):
                # Old section going away
                processSection (rewrite, section_name, section)
                section_name = ""
                section = []
                # New section beginning
                section_name = line.translate (None, '=')
            else:
                section.append (line)
    processSection (rewrite, section_name, section)
    rewrite.close ()

# Read each .wiki file in the current directory
for filename in os.listdir ("."):
    if filename.endswith (".wiki"):
        if filename != 'upload-mapping.wiki':
            processFile (filename)
