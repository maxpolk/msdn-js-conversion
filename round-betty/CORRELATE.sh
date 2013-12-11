#! /bin/sh

#
# Interrupt at high level so that while and for loops actually stop,
# instead of the CHILD process catching the signal and the bash
# script continuing on the next iteration.
#
trap 'exit 2' INT

if [ ! -d "../../msdn-js/" ]; then
    echo "This depends on msdn-js being checked out into ../../msdn-js"
    exit 1
fi

ProcessFile ()
{
    ORIGINAL="$1"
    FILE="$2"

    echo "===== $FILE"
    python special-extract.py "$ORIGINAL" syntaxSection
    # # echo "$FILE"
    # # Look for this:
    # # <div id="syntaxCodeBlocks" class="code">
    # COUNT=$(grep -c '<div id="syntaxCodeBlocks" class="code">' $ORIGINAL)
    # if [ "$COUNT" = "0" ]; then
    #     echo "Not found: $FILE"
    # elif [ "$COUNT" = "1" ]; then
    #     echo -n ""
    # else
    #     echo "BAD: $FILE"
    # fi
    # # sed 's/^.*<div id="syntaxCodeBlocks" class="code">\(.*?\)</div>/\1/' $ORIGINAL
}

/bin/ls ../../msdn-js/*.html | \
    while read file; do
        X=${file//.html}.wiki   # replace file suffix
        X=${X##*msdn-js/}       # strip file prefix path
        if [ -f "$X" ]; then
            ProcessFile "$file" "$X"
        fi
    done
