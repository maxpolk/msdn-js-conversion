#! /bin/sh

grep '||' upload-mapping.wiki | sed 's/^| //' | while read line; do
    FILE="$(echo $line | sed 's/ .*$//')"
    PAGE="$(echo $line | sed 's/^.* || //')"
    echo Upload "$FILE" as "$PAGE"
done
