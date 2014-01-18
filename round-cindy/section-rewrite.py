#! /usr/bin/env python

import os
import sys
import re

# True if we started a syntax section and need to finish it
started_syntax_section = False
finished_syntax_section = False

def addTitleAndFlags (rewrite):
    '''Add the top templates to the file, things like title and flags.'''
    rewrite.write ("{{Page_Title}}\n")
    rewrite.write ("{{Flags}}\n")

def addSummary (rewrite, summary):
    '''Add the summary section template, with given lines of contents.'''
    rewrite.write ("{{Summary_Section|" + "\n".join (summary) + "}}\n")

def addSyntaxHeader (rewrite):
    '''
    Add the JS syntax template header.
    Generate optional content with addSyntaxFormats and addSyntaxValues.
    Finish by calling addsyntaxFooter.
    '''
    # Header
    rewrite.write ("{{JS_Syntax")

def addSyntaxFormats (rewrite, syntax):
    '''Add the JS syntax Format parameter, with given lines of contents.'''
    # Fixed parameter
    rewrite.write ("|Formats=")
    # Repeated lines
    for line in syntax:
        rewrite.write ("{{JS_Object_Format\n")
        rewrite.write ("|Format={}".format (line))
        rewrite.write ("}}")

def addSyntaxValues (rewrite, syntax):
    '''Add the JS syntax Values parameter, with given lines of contents.'''
    # Fixed parameter
    rewrite.write ("\n|Values=")
    # Repeat for each line
    for line in syntax:
        #
        # Split line into name, required, description.  Starts out like:
        #     ; arrayObj: Required. The variable...is assigned.
        # Ends up as:
        #     name         arrayObj
        #     required     Required
        #     description  The variable...is assigned.
        #
        print "{} > [PARAMETER] {}".format ("?", line)
        match = re.match ("^; ([^:]+): *(Optional|Required). *(.*)$", line)
        if match:
            name, required, description = match.group (1, 2, 3)
            rewrite.write ("{{JS_Syntax_Parameter\n")
            rewrite.write ("|Name={}\n".format (name))
            rewrite.write ("|Required={}\n".format (required))
            rewrite.write ("|Description={}".format (description))
            rewrite.write ("}}")
        elif (line is not ""):
            print ("ERROR: could not parse syntax parameter:\n{}".format (line))

def addSyntaxFooter (rewrite):
    '''Finish off the syntax footer.'''
    rewrite.write ("\n}}\n");

def addExamples (rewrite, examples):
    '''Add Examples_Section template instance.'''
    # Fixed parameter
    rewrite.write ("{{Examples_Section\n")
    rewrite.write ("|Examples=" + "\n".join (examples))
    for line in examples:
        print "{} > [EXAMPLES] {}".format ("?", line)
    rewrite.write ("}}\n")

def processSection (filename, rewrite, section_name, section):
    '''
    For given file, process the contents (section: array of lines)
    of the named section (section_name: string) by writing to the
    output rewrite file (rewrite: open file handle).
    '''
    global started_syntax_section, finished_syntax_section
    # Finish off a previous template that has no more information to put into it
    if (started_syntax_section and not finished_syntax_section and
            section_name != "Parameters"):
        addSyntaxFooter (rewrite)
        finished_syntax_section = True
    # Determine if this is the top (unnamed) section
    if section_name == "":
        print "Unnamed top section contains {} lines:".format (len (section))
        addTitleAndFlags (rewrite)
        #
        # Keep track of if we are in the summary section or code example
        # part of the top section.  We can tell because a space is the
        # beginning of the code example.
        #
        past_summary = False
        count = 1
        accum_summary = []
        accum_code = []
        for line in section:
            if past_summary:
                # We are in code example
                print "{} > [CODE] {}".format (count, line)
                accum_code.append (line)
            elif line.startswith (" "):
                # Summary section finished, code example follows
                past_summary = True
                print "{} > [CODE] {}".format (count, line)
                accum_code.append (line)
            else:
                print "{} > [SUMMARY] {}".format (count, line)
                accum_summary.append (line)
            count += 1
        if (len (accum_summary) > 0):
            addSummary (rewrite, accum_summary)
        else:
            print ("WARNING: no summary section")
        if (len (accum_code) > 0):
            # Remember to close off syntax section later
            started_syntax_section = True
            addSyntaxHeader (rewrite)
            addSyntaxFormats (rewrite, accum_code)
        else:
            print ("WARNING: no code section")
    elif (section_name == "Parameters"):
        print "Section \"{}\" contains {} lines:".format (section_name, len (section))
        if (not started_syntax_section):
            print ("ERROR: we never started a syntax template, ignoring Parameters")
        else:
            # This concludes the Syntax template we started above
            addSyntaxValues (rewrite, section)
            addSyntaxFooter (rewrite)
            finished_syntax_section = True
    elif (section_name == "Example"):
        print "Section \"{}\" contains {} lines:".format (section_name, len (section))
        addExamples (rewrite, section)
    else:
        print "Section \"{}\" contains {} lines:".format (section_name, len (section))
        # Write section header
        if section_name != "":
            rewrite.write ("=={}==\n".format (section_name))
        count = 1
        for line in section:
            print "{} > [NORMAL] {}".format (count, line)
            rewrite.write ("{}\n".format (line))
            count += 1

def processFile (filename):
    '''
    Read through a file, separating into mediawiki markup sections.
    Rewrite each section into a new file named with suffix ".rewrite".
    '''
    global started_syntax_section, finished_syntax_section
    started_syntax_section = False
    finished_syntax_section = False

    print ("===== {} =====".format (filename))
    rewrite = open (filename + ".rewrite", 'w')
    section_name = ""
    section = []
    with open (filename) as filein:
        for line in filein:
            line = line.rstrip ("\n")
            if line.startswith ("="):
                # Process section we finished accumulating
                # Strip off empty lines from the end
                while (len (section) > 0 and re.match ('^[ \t]*$', section[-1])):
                    del section[-1]
                if len (section) > 0:
                    processSection (filename, rewrite, section_name, section)
                section_name = ""
                section = []
                # New section beginning
                section_name = line.translate (None, '=')
            else:
                section.append (line)
    # Strip off empty lines from the end
    while (len (section) > 0 and re.match ('^[ \t]*$', section[-1])):
        del section[-1]
    # Process section we finished accumulating
    if len (section) > 0:
        processSection (filename, rewrite, section_name, section)
        rewrite.close ()
    # See if things went well
    if (started_syntax_section and not finished_syntax_section):
        print ("ERROR: started syntax template but didn't finish it")

# Read each .wiki file in the current directory
for filename in os.listdir ("."):
    if filename.endswith (".wiki"):
        processFile (filename)
