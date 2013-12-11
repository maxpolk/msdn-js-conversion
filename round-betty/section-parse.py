#! /usr/bin/env python

import os
import sys
import sys
from xml.etree import ElementTree
import re

def surroundWithSpace (frags, text, tail):
    '''
    Add space before and/or after text depending on context.

    Rule: if preceding fragment doesn't end with space, add preceding space.
    Rule: if tail doesn't begin with space, add trailing space.
    '''
    if (len (frags) > 0 and frags[-1] is not None):
        if (frags[-1][-1] != " " and frags[-1][-1] != "." and frags[-1][-1] != "\n"):
            text = " " + text
    if (tail is not None and tail != "" and tail[0] != " " and tail[0] != "."):
        text = text + " "
    return text

def escapeText (text):
    '''
    Escapes text like | (special table meaning), or {{ (special template meaning),
    or XML chars like < and >.
    '''
    if (text is not None):
        text = text.replace ('{{', '<nowiki>{{</nowiki>')
        text = text.replace ('|', '{{!}}')
        text = text.replace ('&', '&amp;')
        text = text.replace ('<', '&lt;')
        text = text.replace ('>', '&gt;')
        text = text.replace ('>', '&gt;')
    return text

def convertSpanText (element):
    '''
    Given a 'span' element, convert into MediaWiki syntax.

    This is a separate function called from top-level or nested text extraction.
    '''
    elementClass = element.attrib.get ("class")
    if (elementClass is not None and elementClass == "code"):
        # Do not call convertText, infinite recursion, just grab simple text
        return "<code>{:}</code>".format (escapeText (element.text))
    else:
        return escapeText (element.text)

def convertText (element):
    '''
    Given an element such as 'p', convert all the text within it recursively into
    MediaWiki syntax.

    This does more than allText:
    * Turns anchor hrefs into [http://whatever] style text.
    * Escapes special chars like | (table syntax) and < and > (xml syntax)
    '''
    # First you get item.text, then child element, then child element "tail",
    # then next child element, next child element "tail", etc.  The "element.iter()"
    # will go deeper but not tell you, so we get number of children "len (item)"
    # and if there are children, push the tail data off until later in tailStack
    # to be added after the child returns.
    tailStack = []
    frags = []
    for item in element.iter ():
        childrenCount = len (item)
        # Get the text directly inside the element, if empty make it None
        text = escapeText (item.text)
        if (text is not None):
            #text = text.strip ()
            if (text == ""):
                text = None
        # Get the text following the element, if empty make it None
        tail = escapeText (item.tail)
        if (tail is not None):
            #tail = tail.strip ()
            if (tail == ""):
                tail = None
        # If there are children, save the tail data until later
        if (childrenCount > 0):
            tailStack.append (tail) # defer to later
            tail = None             # ignore this for now
        elif (len (tailStack) > 0):
            previousTail = tailStack.pop () # get deferred tail
            if (previousTail is not None):
                tail = previousTail # use it
        # Handle an anchor with a valid href
        if (item.tag == 'a' and text is not None):
            href = item.attrib.get ('href')
            # Turn blank href into None
            if (href is not None):
                href = href.strip ()
                if (href == ""):
                    href = None
            # Convert href into a link
            if (href is not None):
                frags.append (surroundWithSpace (frags, convertLink (href, text), tail))
                if (tail is not None):
                    frags.append (tail)
        elif (item.tag == 'b' and text is not None):
            frags.append (surroundWithSpace (frags, "'''" + text + "'''", tail))
            if (tail is not None):
                frags.append (tail)
        elif (item.tag == 'span' and text is not None):
            frags.append (surroundWithSpace (frags, convertSpanText (item), tail))
            if (tail is not None):
                frags.append (tail)
        elif (item.tag == 'table'):
            # Add separater after a table
            if (len (frags) > 0 and frags[-1] is not None):
                frags.append ('\n\n')
        elif (item.tag == 'th'):
            # Skip table header text
            pass
        else:
            if (text is not None):
                frags.append (surroundWithSpace (frags, text, tail))
            if (tail is not None):
                frags.append (tail)
    # If text fragments were accumulated, join them into a single string
    if (len (frags) == 0):
        return None
    else:
        return ''.join (frags)

def replaceTopExample (original_filename, rewrite):
    '''Write into the rewrite open file the top example section from original.'''
    print "[RECONSTITUTE FROM {}]".format (original_filename)
    # special-extract.py "$ORIGINAL" syntaxSection
    # Parse XML file and find element having given id
    elementid = "syntaxSection"
    tree = ElementTree.parse (original_filename)
    root = tree.getroot ()
    for element in root.findall (".//*[@id='{:}']".format (elementid)):
        converted_text = convertText (element)
        # Prefix all lines with a space
        space_prefixed_text = re.sub ("^", " ", converted_text, flags=re.M)
        # Change ASCII 160 (non-breaking space) into ordinary space
        space_prefixed_text = re.sub (chr(160), ' ', space_prefixed_text)
        print "[REWRITTEN]{}".format (space_prefixed_text)
        rewrite.write ("{}\n".format (space_prefixed_text))

def processSection (filename, rewrite, section_name, section):
    '''For given file, process the contents of the named section.'''
    # Determine if this is the top (unnamed) section
    if section_name == "":
        print "Unnamed top section contains {} lines:".format (len (section))
        past_summary = False
        count = 1
        for line in section:
            if past_summary:
                print "{} > [SKIP] {}".format (count, line)
            elif line.startswith (" "):
                # Summary section finished, code example follows
                past_summary = True
                print "{} > [SKIP] {}".format (count, line)
            else:
                print "{} > [KEEP] {}".format (count, line)
                rewrite.write ("{}\n".format (line))
            count += 1
        # If we skipped code, replace it from the original
        if past_summary:
            # Rewrite code example by pulling in original with better text conversion
            original_filename = "../../msdn-js/" + filename.replace (".wiki", ".html")
            original_filename = original_filename.replace (
                "Conditional__Ternary-Operator.html",
                "Conditional__Ternary)-Operator.html")
            original_filename = original_filename.replace (
                "Increment-and-Decrement-Operators.html",
                "Increment.html")
            original_filename = original_filename.replace (
                "Modulus-Assignment-Operator.html",
                "Modulus-Assignment-Operator-.html")
            replaceTopExample (original_filename, rewrite)
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
                # Old section going away
                if len (section) > 0:
                    processSection (filename, rewrite, section_name, section)
                section_name = ""
                section = []
                # New section beginning
                section_name = line.translate (None, '=')
            else:
                section.append (line)
    if len (section) > 0:
        processSection (filename, rewrite, section_name, section)
        rewrite.close ()

# Read each .wiki file in the current directory
for filename in os.listdir ("."):
    if filename.endswith (".wiki"):
        if filename != 'upload-mapping.wiki':
            processFile (filename)
