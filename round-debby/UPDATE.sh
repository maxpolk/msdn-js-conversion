#! /bin/sh

IFS=$'\n'
for LINE in $(<REFINED-OUTPUT.txt); do
    PAGE=${LINE/ | */}
    URL=${LINE/* | /}
    PAGE=${PAGE%% }
    PAGE=${PAGE%% }
    # echo "$PAGE: "
    # Replace encoded filename with actual page name
    TARGET=$PAGE
    TARGET=${TARGET// /_}
    TARGET=${TARGET//\//.}
    TARGET=${TARGET}.wiki
    # echo "    $TARGET"
    FILE="../round-cindy/javascript.$TARGET"
    if [ ! -f "$FILE" ]; then
        echo "Could not find:  ${TARGET%%.wiki}"
    elif [ ! -f "${FILE}.rewrite" ]; then
        echo "Missing rewrite: ${FILE}.rewrite"
    else
        REWRITE="${FILE}.rewrite"
        # Fix URL
        URL="http://msdn.microsoft.com$URL"
        # Escape sed special chars
        URL=${URL//\//\\\/}
        sed -i "s/MSDN_link=.*\$/MSDN_link=${URL}/" "$REWRITE"
    fi
done
