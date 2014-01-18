#! /usr/bin/env python

import os
import sys
import re

#
# REWRITE RULES
#

# {{Page_Title}}

# {{Flags}}

# THIS (first part of top unnamed section prior to code):
# Provides support for creation of arrays of any data type.
# BECOMES:
# {{Summary_Section|Provides support for creation of arrays of any data type.}}

# THIS (leading space, top unnamed section):
#  arrayObj = new Array()
#  arrayObj = new Array([ size ])
#  arrayObj = new Array([ element0 [, element1 [, ...[, elementN ]]]])
# BECOMES (each line goes into JS_Syntax Formats / JS_Object_Format)
# {{JS_Syntax
# |Formats={{JS Object Format
# |Format=arrayObj = new Array();
# }}{{JS Object Format
# |Format=arrayObj = new Array([ size ]);
# }}{{JS Object Format
# |Format=arrayObj = new Array([ element0 [, element1 [, ...[, elementN ]]]]);
# }}

# THIS (Parameters section, stuff beginning with ; PARAMETER: ):
# ; arrayObj: Required. The variable name to which the '''Array''' object is assigned.
# ; size: Optional. The size of the array. As arrays are zero-based, created elements will have indexes from zero to size -1.
# ; element0,...,elementN: Optional. The elements to place in the array. This creates an array with n + 1 elements, and a '''length''' of n + 1. Using this syntax, you must supply more than one element.
# BECOMES (each line goes into Values/ JS_Syntax_Parameter, split into Name, Required, Description):
# |Values={{JS Syntax Parameter
# |Name=arrayObj
# |Required=Yes
# |Description=The variable name to which the '''Array''' object is assigned.
# }}{{JS Syntax Parameter
# |Name=size
# |Required=No
# |Description=The size of the array. As arrays are zero-based, created elements will have indexes from zero to size -1.
# }}{{JS Syntax Parameter
# |Name=element0,...,elementN
# |Required=No
# |Description=The elements to place in the array. This creates an array with n + 1 elements, and a '''length''' of n + 1. Using this syntax, you must supply more than one element.
# }}

# ALSO we close off the JS_Syntax whether or not we have a Parameters section:
# }}

# THIS (Examples section):
# The following example illustrates the use of the '''0 . . .''' n properties of the '''arguments''' object. To fully understand the example, pass one or more arguments to the function:
# 
#  function ArgTest(){
#     var s = "";
#     s += "The individual arguments are: "
#     for (n = 0; n &lt; arguments.length; n++){
#        s += ArgTest.arguments[n] ;
#        s += " ";
#     }
#     return(s);
#  }
#  document.write(ArgTest(1, 2, "hello", new Date()));
# }}
# BECOMES:
# {{Examples_Section
# |Examples=
# The following example illustrates the use of the '''0 . . .''' n properties of the '''arguments''' object. To fully understand the example, pass one or more arguments to the function:
# 
#  function ArgTest(){
#     var s = "";
#     s += "The individual arguments are: "
#     for (n = 0; n &lt; arguments.length; n++){
#        s += ArgTest.arguments[n] ;
#        s += " ";
#     }
#     return(s);
#  }
#  document.write(ArgTest(1, 2, "hello", new Date()));
# }}

def processSection (filename, rewrite, section_name, section):
    '''
    For given file, process the contents (section: array of lines)
    of the named section (section_name: string) by writing to the
    output rewrite file (rewrite: open file handle).
    '''
    # Determine if this is the top (unnamed) section
    if section_name == "":
        print "Unnamed top section contains {} lines:".format (len (section))
        #
        # Keep track of if we are in the summary section or code example
        # part of the top section.  We can tell because a space is the
        # beginning of the code example.
        #
        past_summary = False
        count = 1
        for line in section:
            if past_summary:
                # We are in code example
                print "{} > [CODE] {}".format (count, line)
            elif line.startswith (" "):
                # Summary section finished, code example follows
                past_summary = True
                print "{} > [CODE] {}".format (count, line)
            else:
                print "{} > [SUMMARY] {}".format (count, line)
                rewrite.write ("{}\n".format (line))
            count += 1
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
    print ("===== {} =====".format (filename))
    rewrite = open (filename + ".rewrite", 'w')
    section_name = ""
    section = []
    with open (filename) as filein:
        for line in filein:
            line = line.rstrip ("\n")
            if line.startswith ("="):
                # Process section we finished accumulating
                if len (section) > 0:
                    processSection (filename, rewrite, section_name, section)
                section_name = ""
                section = []
                # New section beginning
                section_name = line.translate (None, '=')
            else:
                section.append (line)
    # Process section we finished accumulating
    if len (section) > 0:
        processSection (filename, rewrite, section_name, section)
        rewrite.close ()

# Read each .wiki file in the current directory
for filename in os.listdir ("."):
    if filename.endswith (".wiki"):
        if filename != 'upload-mapping.wiki':
            processFile (filename)
