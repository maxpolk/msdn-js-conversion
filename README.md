msdn-js-conversion
==================

Scripts to convert MSDN JavaScript HTML page contributions to Web Platform Docs.

This is special one-time project work.  The driver script is the
"complete-convert" bash script.  Run that from somewhere outside of this
directory, because it will issue a git clone command to obtain the source
HTML then begin converting.

To run it, edit setenv.sh to point to the wiki you choose, as well as enter
the wiki username and password used to push new versions of pages to that wiki.

Then source the setenv.sh and run the complete-convert script:

    . setenv.sh
    cd ..
    msdn-js-conversion/complete-convert

That will kick off the entire conversion process.  First it will clone
from github the source HTML files (if not already cloned) then begin
converting in phases.  If successful you will see a SUCCESS at the end.
