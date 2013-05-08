msdn-js-conversion
==================

Scripts to convert MSDN Javascript page contribution to Web Platform Docs.

The driver script is the "complete-convert" bash script.  Run that from
somewhere OUTSIDE of this directory, because it will issue a git clone
command to obtain the source HTML.

For example, run this:

    Edit setenv.sh to point to the wiki you choose, and set username/password.
    . setenv.sh
    cd ..
    msdn-js-conversion/complete-convert

That will kick off the entire conversion process.  First it will clone
from github the source HTML files (if not already cloned) then begin
converting in phases.  If successful you will see a SUCCESS at the end.
