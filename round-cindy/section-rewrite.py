#! /usr/bin/env python

import os
import sys
import re

#: For each file, true if we started a syntax section and need to finish it
started_syntax_section = False

#: If we added the |Values= parameter yet
added_values_param = False

#: For each file, true if we finished a syntax section
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
    # Sometimes it is a simple sentence, sometimes a formatted definition list entry
    if (len (syntax) == 1 and not syntax[0].startswith ("; ")):
        print ("Unusual syntax line: {}".format (syntax[0]))
        rewrite.write ("{{JS_Syntax_Parameter\n")
        rewrite.write ("|Name={}\n".format (""))
        rewrite.write ("|Required={}\n".format (""))
        rewrite.write ("|Description={}".format (syntax[0]))
        rewrite.write ("}}")
    else:
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
                if (required == "Required"):
                    required = "true"
                else:
                    required = "false"
                rewrite.write ("{{JS_Syntax_Parameter\n")
                rewrite.write ("|Name={}\n".format (name))
                rewrite.write ("|Required={}\n".format (required))
                rewrite.write ("|Description={}".format (description))
                rewrite.write ("}}")
            elif (line is not ""):
                match = re.match ("^; ([^:]+): *(.*)$", line)
                if match:
                    name, description = match.group (1, 2)
                    required = "false"
                    rewrite.write ("{{JS_Syntax_Parameter\n")
                    rewrite.write ("|Name={}\n".format (name))
                    rewrite.write ("|Required={}\n".format (required))
                    rewrite.write ("|Description={}".format (description))
                    rewrite.write ("}}")
                else:
                    rewrite.write ("{{JS_Syntax_Parameter\n")
                    rewrite.write ("|Name={}\n".format (""))
                    rewrite.write ("|Required={}\n".format (""))
                    rewrite.write ("|Description={}".format (line))
                    rewrite.write ("}}")
            else:
                    rewrite.write ("{{JS_Syntax_Parameter\n")
                    rewrite.write ("|Name={}\n".format (""))
                    rewrite.write ("|Required={}\n".format (""))
                    rewrite.write ("|Description={}".format (line))
                    rewrite.write ("}}")

def addReturnValue (rewrite, syntax):
    '''Add a return value as a JS syntax Values parameter, with given line of content.'''
    # Sometimes it is a simple sentence, sometimes a formatted definition list entry
    print ("Return value syntax line: {}".format (syntax[0]))
    rewrite.write ("{{JS_Syntax_Parameter\n")
    rewrite.write ("|Name={}\n".format ("return value"))
    rewrite.write ("|Required={}\n".format (""))
    rewrite.write ("|Description={}".format (syntax[0]))
    rewrite.write ("}}")

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

def convertParameters (parameters):
    '''Convert parameters in wikitable format to Mediawiki definition list.'''
    # If it's already in the right format, do nothing
    if (len (parameters) > 0 and len (parameters[0]) > 0 and parameters[0][0] == ';'):
        print ("Parameters section does not need converting")
        return
    if (len (parameters) == 1 and parameters[0][0] != ';'):
        print ("Parameters section is simple and does not need converting")
        return
    print ("Parameters section REWRITE")
    #
    # BEFORE:
    # {| class='wikitable'
    # |-
    # ! Parameter
    # ! Definition
    # |-
    # | array1
    # | Required. An array object.
    # |-
    # | callbackfn
    # | Required. A function that accepts up to three ...
    # |-
    # | thisArg
    # | Optional. An object to which the this keyword ...
    # |}
    # AFTER:
    # ; array1: Required. An array object.
    # ; callbackfn: Required. A function that accepts up to three ...
    # ; thisArg: Optional. An object to which the this keyword ...
    #
    if (len (parameters) < 5):
        print ("ERROR: malformed parameters section: len (parameters) < 5:")
        print ("{}".format ("\n".join (parameters)))
        return
    del parameters[0]
    if (parameters[0] != "|-"):
        print ("ERROR: malformed parameters section: parameters[0] != '|-'")
        return
    del parameters[0]
    if (parameters[0] != "! Parameter"):
        print ("ERROR: malformed parameters section: parameters[0] != '! Parameter'")
        return
    del parameters[0]
    if (parameters[0] != "! Definition"):
        print ("ERROR: malformed parameters section: parameters[0] != '! Definition'")
        return
    del parameters[0]
    if (parameters[0] != "|-"):
        print ("ERROR: malformed parameters section: parameters[0] != '|-'")
        return
    del parameters[0]
    # Grab 3 lines at a time to convert
    accum = []
    while (len (parameters) >= 3):
        # BEFORE:
        # | array1
        # | Required. An array object.
        # |-  or  |}
        # AFTER:
        # ; array1: Required. An array object.
        name = parameters[0][2:]
        print (">> CONVERT: {} to: {}".format (parameters[0], name))
        del parameters[0]
        description = parameters[0][2:]
        print (">> CONVERT: {} to: {}".format (parameters[0], description))
        del parameters[0]
        print (">> IGNORE: {}".format (parameters[0]))
        del parameters[0]
        accum.append ("; {}: {}".format (name, description))
        print (">> NEW VALUE: {}".format (accum[-1]))
    if (len (parameters) != 0):
        print ("ERROR: parameters not empty:\n{}".format ("\n".join (parameters)))
    parameters += accum

def processSection (filename, rewrite, section_name, section):
    '''
    For given file, process the contents (section: array of lines)
    of the named section (section_name: string) by writing to the
    output rewrite file (rewrite: open file handle).
    '''
    global started_syntax_section, finished_syntax_section, added_values_param
    # Finish off a previous template that has no more information to put into it
    if (started_syntax_section and not finished_syntax_section and
            section_name != "Parameters" and section_name != "Return Value"):
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
        # Convert old table structure to new definition list structure
        convertParameters (section)
        print "Section \"{}\" contains {} lines:".format (section_name, len (section))
        if (not started_syntax_section):
            print ("ERROR: we never started a syntax template, ignoring {}".format (
                section_name))
        else:
            # This concludes the Syntax template we started above
            added_values_param = True
            addSyntaxValues (rewrite, section)
    elif (section_name == "Return Value"):
        print "Section \"{}\" contains {} lines:".format (section_name, len (section))
        if (not started_syntax_section):
            print ("ERROR: we never started a syntax template, ignoring {}".format (
                section_name))
        elif (not added_values_param):
            addSyntaxValues (rewrite, section)
        else:
            addReturnValue (rewrite, section)
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

def addFooter (rewrite):
    # Enable semantic forms
    rewrite.write ("{}\n".format ("{{Basic Page}}"))

def processFile (filename):
    '''
    Read through a file, separating into mediawiki markup sections.
    Rewrite each section into a new file named with suffix ".rewrite".
    '''
    global started_syntax_section, finished_syntax_section, added_values_param
    started_syntax_section = False
    added_values_param = False
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
    # Strip off empty lines from the end
    while (len (section) > 0 and re.match ('^[ \t]*$', section[-1])):
        del section[-1]
    if len (section) > 0:
        processSection (filename, rewrite, section_name, section)
    # Finish off a previous template that has no more information to put into it
    if (started_syntax_section and not finished_syntax_section):
        addSyntaxFooter (rewrite)
        finished_syntax_section = True
    # Write page footer
    addFooter (rewrite)
    rewrite.close ()

if __name__ == '__main__':
    # Read each .wiki file in the current directory
    for filename in os.listdir ("."):
        if filename.endswith (".wiki"):
            processFile (filename)
