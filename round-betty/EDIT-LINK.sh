#! /bin/sh

if [ ! "$#" = "2" ]; then
    echo "Usage: EDIT-LINK.sh LINK NEWLINK"
    exit 1
fi
LINK="$1"
NEWLINK="$2"
echo "Fixing link $LINK"

# Escape the slashes inside the LINK and NEWLINK
LINK=$(echo "$LINK" | sed s'/\//\\\//g')
NEWLINK=$(echo "$NEWLINK" | sed s'/\//\\\//g')

for file in $(grep -l "\[\[${LINK}" *.wiki); do
    echo "    $file"
    sed -i "s/\[\[${LINK}|/\[\[${NEWLINK}|/g" $file
done
