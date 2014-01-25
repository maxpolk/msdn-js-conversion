Copy *.wiki files from ../round-betty into this directory.

Run RENAME.sh

Run PROCESS-ORIGINAL.sh

Run python section-rewrite.py

[OPTIONAL] Delete existing pages that are in the way (repeat until no more):
  ../modified-wpd ls javascript 100 | tee DELETE.pages
  ../modified-wpd batchdelete DELETE.pages "Delete to prepare for batch upload"

Run upload.sh
