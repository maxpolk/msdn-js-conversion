#! /bin/sh

#
# Fix internal links within files according to the following rules:
#
#   Remove the suffix " Function", " Method", " Property"
#
echo "Fix internal links within files"
for file in *.wiki; do
    echo "    $file"
    if [ "$file" = "upload-mapping.wiki" ]; then
        echo "Ignoring non-content file"
        continue
    fi

    #
    # Change this:
    #     [[Objects/Object/toString Method|toString method]]
    # To this:
    #     [[Objects/Object/toString|toString method]]
    # Do the same for " Function", " Method", " Property"
    #
    sed -i -r -e "s/(\[\[[^]\|]*) (Function|Method|Property)([]\|].*$)/\1\3/" $file
done
