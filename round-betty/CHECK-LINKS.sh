#! /bin/sh

# Process a link found in a file
processlink ()
{
    FILE="$1"
    LINE="$2"
    if ! echo "$LINE" | grep -q '|'; then
        echo "ERROR ($FILE): DID NOT find bar char in link $LINE"
        exit 1
    fi

    # Turn line into link
    LINK=$(echo "$LINE" | sed 's/\[\[\(.*\)|.*$/\1/')

    #
    # See if link is in upload-mapping.wiki
    # Example link:
    #     javascript/future reserved words
    # Example line in upload-mapping.wiki:
    #     | JavaScript-Future-Reserved-Words.wiki || javascript/future reserved words
    #
    if ! grep -q "|| ${LINK}\$" upload-mapping.wiki; then
        echo "Bad link: $LINK"
    fi
}

# Find all links inside all files
for file in $(/bin/ls *.wiki | grep -v upload-mapping); do
    # Search for [[
    # Then split multiple links in one line into separate lines
    # Then eliminate all lines that don't begin with [[
    # Then eliminate everything after the last ]]
    # Then pass it along to the processlink function
    grep '\[\[' $file | \
        sed 's/\(\[\[\)/\n\1/g' | \
        grep '^\[\[' | \
        sed 's/\(\]\]\).*$/\1/' | \
        while read link; do processlink "$file" "$link"; done
done
