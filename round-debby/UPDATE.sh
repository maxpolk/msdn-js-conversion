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
        echo "    ${TARGET%%.wiki}"
    fi
done
