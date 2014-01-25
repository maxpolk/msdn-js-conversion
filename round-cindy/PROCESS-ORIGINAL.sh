#! /bin/sh

trap 'exit 2' INT

# Walk through each original file
cat MAP-ORIGINAL.txt | \
    while read HTML WIKI; do
        # Ensure both files exist
        if [ ! -f ../../msdn-js/$HTML ]; then
            echo "ERROR: did not find $HTML"
        fi

        if [ ! -f $WIKI ]; then
            echo "ERROR: did not find $WIKI"
        fi

        #
        # Look in see also section for things like this:
        #     <a href="SOMETHING.htm">Array Object (JavaScript)</a>
        # Grab the "SOMETHING" and anchor text, make it look like:
        #     08e5f552-0797-4b48-8164-609582fc18c9 Array Object (JavaScript)
        #
        python get-fragment.py "../../msdn-js/$HTML" seeAlsoSection | \
            grep '<a ' | \
            sed 's/^.*href="\(.*\).htm">\(.*\)<\/a>.*$/\1 "\2"/' | (
                read LINK TITLE
                # Strip quotes from around TITLE
                TITLE=${TITLE//\"/}
                if [ ! -z "$LINK" ]; then
                    echo "----------"
                    echo "WIKI is $WIKI"
                    echo "LINK is $LINK"
                    echo "TITLE is $TITLE"
                    # Fix title syntax
                    ORIGINAL_TITLE=$TITLE
                    TITLE=${TITLE//&amp;/&#38;}
                    TITLE=${TITLE//&lt;/&#60;}
                    TITLE=${TITLE//&gt;/&#62;}
                    # Passing to grep, escape regex special char
                    TITLE=${TITLE//\*/\\*}
                    # TITLE=${TITLE//[/\\[}
                    # TITLE=${TITLE//]/\\]}
                    # Find the title in all other files, should match just one page
                    PAGE1=$(grep -l "<title>$TITLE</title>" ../../msdn-js/*.html)
                    PAGE2=$(grep -l "<meta name=\"Microsoft.Help.Id\" content=\"$LINK\" />" ../../msdn-js/*.html)
                    PAGE1=${PAGE1##../../msdn-js/}
                    PAGE2=${PAGE2##../../msdn-js/}
                    if [ "$PAGE1" = "$PAGE2" ]; then
                        # See if we match something in the MAP-ORIGINAL.txt
                        TARGET=$(grep "^$PAGE1 " MAP-ORIGINAL.txt | sed 's/^.*  *//')
                        if [ -f "$TARGET" ]; then
                            echo "TARGET is $TARGET"
                        else
                            echo "Could not find TARGET $TARGET"
                        fi
                        # Add the "see also" section to bottom of wiki page
                    else
                        echo "PAGES do not match"
                        echo "    $PAGE1"
                        echo "    $PAGE2"
                    fi
                fi
            )
    done
