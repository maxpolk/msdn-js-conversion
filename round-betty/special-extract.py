#! /usr/bin/env python
'''
Extract top example code from an html file.
'''

import sys
from xml.etree import ElementTree

usage = "Usage: special-extract.py INPUTFILE ELEMENTID"

# Parse args
if len (sys.argv) != 3:
    raise Exception ("ERROR: Invalid number of arguments\n{:}".format (usage))
inputfile = sys.argv[1]
elementid = sys.argv[2]

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

# Parse XML file and find element having given id
tree = ElementTree.parse (inputfile)
root = tree.getroot ()
for element in root.findall (".//*[@id='{:}']".format (elementid, elementid)):
    print (convertText (element))
