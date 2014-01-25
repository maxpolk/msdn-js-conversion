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
        unset RESULT
        declare -a RESULT
        IFS=$'\n'
        RESULT=($(python get-fragment.py "../../msdn-js/$HTML" seeAlsoSection | \
            grep '<a ' | \
            sed 's/^.*href="\(.*\).htm">\(.*\)<\/a>.*$/\1~\2/'))
        if [ ${#RESULT[@]} -gt 0 ]; then
            echo "-----"
            echo "HTML=$HTML"
            echo "WIKI=$WIKI"
            # Add "see also" section if not already there
            if ! grep -q '==See Also==' $WIKI; then
                echo "    SECTION ADD of see also"
                echo >> $WIKI
                echo "==See Also==" >> $WIKI
            fi
            for ITEM in ${RESULT[@]}; do
                # Line has format SOMETHING~Title with spaces
                LINK=${ITEM/~*/}
                TITLE=${ITEM/*~/}
                echo "    LINK=$LINK"
                echo "    TITLE=$TITLE"
                # Fix title syntax
                TITLE=${TITLE//&amp;/&#38;}
                TITLE=${TITLE//&lt;/&#60;}
                TITLE=${TITLE//&gt;/&#62;}
                # Passing to grep, so escape regex special char
                TITLE=${TITLE//\*/\\*}
                # TITLE=${TITLE//[/\\[}
                # TITLE=${TITLE//]/\\]}
                # Find the title in all other files, should match just one page
                PAGE1=$(grep -l "<title>$TITLE</title>" ../../msdn-js/*.html)
                PAGE2=$(grep -l "<meta name=\"Microsoft.Help.Id\" content=\"$LINK\" />" ../../msdn-js/*.html)
                PAGE1=${PAGE1##../../msdn-js/}
                PAGE2=${PAGE2##../../msdn-js/}
                if [ ! "$PAGE1" = "$PAGE2" ]; then
                    echo "    PAGES do not match"
                    echo "        $PAGE1"
                    echo "        $PAGE2"
                    continue
                fi
                # See if we match something in the MAP-ORIGINAL.txt
                TARGET=$(grep "^$PAGE1 " MAP-ORIGINAL.txt | sed 's/^.*  *//')
                if [ -f "$TARGET" ]; then
                    echo "    TARGET is $TARGET"
                else
                    echo "    Could not find TARGET $TARGET"
                fi
                # Replace encoded filename with actual page name
                TARGET=${TARGET//.wiki/}
                TARGET=${TARGET//./\/}
                TARGET=${TARGET//_/ }
                # Remove (JavaScript) from the end
                TITLE=${TITLE// (JavaScript*/}
                # Write new "see also" link
                echo "[[$TARGET|$TITLE]]" >> $WIKI
            done
        fi
        unset IFS
    done
