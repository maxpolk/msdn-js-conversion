Assuming you have a script named "rhino", such as a script like:

    #! /bin/sh
    java -jar 'C:\SomeDirectroy\rhino\js.jar' "$@"

Run:
    EXTRACT.js > OUTPUT.txt

Run:
    REWRITE.pl | tr -d $'\r' > REFINED-OUTPUT.txt

Run:
    UPDATE.sh
