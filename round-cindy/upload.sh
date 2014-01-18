#! /bin/sh

if [ -z "$WPD_USERNAME" ]; then
    echo "Missing environment variable WPD_USERNAME"
    exit 1
fi

if [ -z "$WPD_PASSWORD" ]; then
    echo "Missing environment variable WPD_PASSWORD"
    exit 1
fi

if [ -z "$WPD_API_ROOT" ]; then
    echo "Missing environment variable WPD_API_ROOT"
    exit 1
fi

#
# Files with .wiki extension are named after a convention that captures
# the page name in the file name:
#     Period becomes slash
#     Underscore becomes space
#
for FILE in *.wiki; do
    PAGE="$(echo $FILE | sed -e 's/\./\//g' -e 's/_/ /g')"
    echo ../modified-wpd edit \""$PAGE"\" \""$FILE"\" 'Script automated upload'
    ../modified-wpd edit \""$PAGE"\" \""$FILE"\" 'Script automated upload'
done
