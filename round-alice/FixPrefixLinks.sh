#! /bin/sh

#
# Remove prefix "Objects/" from internal links within files
#
echo "Remove prefix Objects/ from internal links within files"
for file in *.wiki; do
    echo "    $file"
    if [ "$file" = "upload-mapping.wiki" ]; then
        echo "Ignoring non-content file"
        continue
    fi

    #
    # Change this:
    #     [[Objects/Object/toString|toString method]]
    # To this:
    #     [[Object/toString|toString method]]
    #
    sed -i -r -e "s/(\[\[)Objects\//\1/g" $file
done
