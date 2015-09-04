#!/bin/bash
for file in $1*
do
    echo "----->>>>>----->>>>>----->>>>>"
    echo $file
    echo "/bin/bash upload.sh \"$file\""
    /bin/bash upload.sh "$file"
    echo "python jones.py \"$file\""
    python jones.py "$file"
done
