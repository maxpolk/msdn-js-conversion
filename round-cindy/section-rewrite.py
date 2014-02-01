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

def escape (line):
    '''
    Escape the bar character anywhere inside the line, and add a space
    after each table end so it is not run together next to a template close
    double right curly brace which mediawiki can't handle.  Hopefully
    people won't edit out the trailing space in the form edit to undo
    this fix.
    '''
    return line.replace ("|}", "|} ").replace ("|", "{{!}}")

def addTitleAndFlags (rewrite):
    '''Add the top templates to the file, things like title and flags.'''
    rewrite.write ("{{Page_Title}}\n")
    rewrite.write ("{{Flags}}\n")

def addSummary (rewrite, summary):
    '''Add the summary section template, with given lines of contents.'''
    rewrite.write ("{{Summary_Section|")
    for line in summary:
        rewrite.write ("{}\n".format (escape (line)))
    rewrite.write ("}}\n")

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
        rewrite.write ("{{JS_Syntax_Format\n")
        rewrite.write ("|Format={}".format (escape (line)))
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
        rewrite.write ("|Description={}".format (escape (syntax[0])))
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
                    required = "Required"
                else:
                    required = "Optional"
                rewrite.write ("{{JS_Syntax_Parameter\n")
                rewrite.write ("|Name={}\n".format (escape (name)))
                rewrite.write ("|Required={}\n".format (escape (required)))
                rewrite.write ("|Description={}".format (escape (description)))
                rewrite.write ("}}")
            elif (line is not ""):
                match = re.match ("^; ([^:]+): *(.*)$", line)
                if match:
                    name, description = match.group (1, 2)
                    required = ""
                    rewrite.write ("{{JS_Syntax_Parameter\n")
                    rewrite.write ("|Name={}\n".format (escape (name)))
                    rewrite.write ("|Required={}\n".format (escape (required)))
                    rewrite.write ("|Description={}".format (escape (description)))
                    rewrite.write ("}}")
                else:
                    rewrite.write ("{{JS_Syntax_Parameter\n")
                    rewrite.write ("|Name={}\n".format (""))
                    rewrite.write ("|Required={}\n".format (""))
                    rewrite.write ("|Description={}".format (escape (line)))
                    rewrite.write ("}}")
            else:
                    rewrite.write ("{{JS_Syntax_Parameter\n")
                    rewrite.write ("|Name={}\n".format (""))
                    rewrite.write ("|Required={}\n".format (""))
                    rewrite.write ("|Description={}".format (escape (line)))
                    rewrite.write ("}}")

def addReturnValue (rewrite, syntax):
    '''
    Add return value as a special template instance.
        {{JS Return Value
        |Description=
        }}
    '''
    print ("Return value syntax line: {}".format ("\n".join(syntax)))
    rewrite.write ("{{JS_Return_Value\n")
    rewrite.write ("|Description={}".format (escape ("\n".join(syntax))))
    rewrite.write ("}}\n")

def addSyntaxFooter (rewrite):
    '''Finish off the syntax footer.'''
    rewrite.write ("\n}}\n");

def addExamples (rewrite, examples):
    '''Add Examples_Section template instance.'''
    # Fixed parameter
    rewrite.write ("{{Examples_Section\n")
    rewrite.write ("|Not_required=No\n")
    rewrite.write ("|Examples=")

    #
    # The Examples parameter has multiple Single_Example template instances.
    # The Single_Example has Code and Description and Language JavaScript.
    #
    # A flag toggles between Description and Code, once we flip from
    # Code to non-code, we begin another Single_Example.
    #
    #{{Single_Example
    # |Language=JavaScript
    # |Description=The following example illustrates the use of the '''0 . . .''' n properties of the '''arguments''' object. To fully understand the example, pass one or more arguments to the function:
    # |Code= function ArgTest(){
    #     var s = "";
    #     s += "The individual arguments are: "
    #     for (n = 0; n &lt; arguments.length; n++){
    #        s += ArgTest.arguments[n] ;
    #        s += " ";
    #     }
    #     return(s);
    #  }
    #  document.write(ArgTest(1, 2, "hello", new Date()));}}
    #}}
    inside_template = False
    inside_description = False
    inside_code = False
    current_line_is_code = False
    current_line_is_blank = False
    for line in examples:
        # Might need to start a new Single Example template instance
        if (not inside_template):
            # Begin a new Single Example
            inside_template = True
            inside_description = False
            inside_code = False
            rewrite.write ("{{Single_Example\n")
            rewrite.write ("|Language=JavaScript\n")

        # Determine if this is code or description
        if (len (line) == 0):
            current_line_is_blank = True
        elif (line[0] == " "):
            current_line_is_blank = False
            current_line_is_code = True
        else:
            current_line_is_blank = False
            current_line_is_code = False

        #
        # If we have a non-blank line, and we were in code and now find
        # a description, begin a new template instance
        #
        if (not current_line_is_blank and inside_code and not current_line_is_code):
            if (inside_template):
                # Close off previous template
                inside_template = False
                rewrite.write ("}}")
            # Begin a new Single Example
            inside_template = True
            inside_description = False
            inside_code = False
            rewrite.write ("{{Single_Example\n")
            rewrite.write ("|Language=JavaScript\n")

        # Nothing to something
        if (not inside_description and not inside_code):
            # Add a template parameter (Description or Code)
            if (current_line_is_code):
                rewrite.write ("|Code=")
                inside_code = True
            else:
                rewrite.write ("|Description=")
                inside_description = True
        elif (inside_description and current_line_is_code):
            # Flip from description to code
            rewrite.write ("|Code=")
            inside_description = False
            inside_code = True

        # Write current line
        rewrite.write ("{}\n".format (escape (line)))
        print "{} > [EXAMPLES] {}".format ("?", line)
    # Finish off the Single_Example
    if inside_template:
        rewrite.write ("}}")
    # Finish off the Examples_Section
    rewrite.write ("}}\n")

def addRemarks (rewrite, remarks):
    '''Add Remarks_Section template instance.'''
    # Fixed parameter
    rewrite.write ("{{Remarks_Section\n")
    rewrite.write ("|Remarks=")
    for line in remarks:
        rewrite.write ("{}\n".format (escape (line)))
        print "{} > [REMARKS] {}".format ("?", line)
    rewrite.write ("}}\n")

def addSeeAlso (rewrite, see_also):
    '''
    Add See_Also_Section template instance.

    Must have bullet in front of each link as in:
        {{See_Also_Section
        |Manual_links=* [http://www.google.com Google]
        * [http://www.mozilla.org Mozilla]
        * [http://www.opera.com Opera]
        }}
    '''
    # Fixed parameter
    rewrite.write ("{{See_Also_Section\n")
    rewrite.write ("|Manual_links=")
    for line in see_also:
        rewrite.write ("* {}\n".format (escape (line)))
        print "{} > [SEE ALSO] {}".format ("?", line)
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
        addReturnValue (rewrite, section)
    elif (section_name == "Example"):
        print "Section \"{}\" contains {} lines:".format (section_name, len (section))
        addExamples (rewrite, section)
    elif (section_name == "Remarks"):
        print "Section \"{}\" contains {} lines:".format (section_name, len (section))
        addRemarks (rewrite, section)
    elif (section_name == "See Also"):
        print "Section \"{}\" contains {} lines:".format (section_name, len (section))
        addSeeAlso (rewrite, section)
    else:
        print "Section \"{}\" contains {} lines:".format (section_name, len (section))
        # Write section header
        if section_name != "":
            rewrite.write ("=={}==\n".format (section_name))
        count = 1
        for line in section:
            print "{} > [NORMAL] {}".format (count, line)
            # Not escaping line, no need to since it's not inside a template
            rewrite.write ("{}\n".format (line))
            count += 1

def addFooter (rewrite):
    # Enable semantic forms
    rewrite.write ("{}\n".format ("{{Topics | JS Basic}}"))

    # Add an external attribution to MSDN
    rewrite.write ("{}\n".format ('''
{{External_Attribution
|Is_CC-BY-SA=No
|Sources=MSDN
|MDN_link=
|MSDN_link=http://msdn.microsoft.com/en-us/library/ie/yek4tbz0%28v=vs.94%29.aspx Windows Internet Explorer JavaScript reference
|HTML5Rocks_link=
}}'''))

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
                # Strip off empty lines from the beginning
                while (len (section) > 0 and re.match ('^[ \t]*$', section[0])):
                    del section[0]
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
    # Strip off empty lines from the beginning
    while (len (section) > 0 and re.match ('^[ \t]*$', section[0])):
        del section[0]
    # Strip off empty lines from the end
    while (len (section) > 0 and re.match ('^[ \t]*$', section[-1])):
        del section[-1]
    # Process section we finished accumulating
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
