#! /bin/sh

# Ensure { and } count match in all files
for file in *.rewrite; do
    echo -n "$file: "
    histogram-python --chars < $file | \
        grep -e '^[{}]' | \
        sed 's/^.: //' | \
        sort | uniq | wc -l
done
