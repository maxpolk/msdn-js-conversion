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

# Import path prefix
PREFIX="Tests/javascript-b"

grep '||' upload-mapping.wiki | sed 's/^| //' | while read line; do
    FILE="$(echo $line | sed 's/ .*$//')"
    PAGE="$(echo $line | sed 's/^.* || //')"
    echo ../modified-wpd edit \""$PREFIX/$PAGE"\" \""$FILE"\" 'Script automated upload'
    ../modified-wpd edit "$PREFIX/$PAGE" "$FILE" 'Script automated upload'
done
