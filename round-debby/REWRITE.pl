#! /usr/bin/perl -w
use strict;

grep {
    chomp;
    my $line = $_;

    # Remove the suffix " Function", " Method", " Property"
    $line =~ s/ \((Function|Method|Property)\) / /;

    # Replace prefixes
    $line =~ s/^JavaScript Directives/directives/;
    $line =~ s/^JavaScript Errors/errors/;
    $line =~ s/^JavaScript Reserved Words/reserved words/;
    $line =~ s/^JavaScript Objects\/([^\/]+) Object/$1/;
    $line =~ s/^JavaScript Statement\/([^ ]+) Statement/$1/;
    $line =~ s/^Regular Expression/regular expression/;
    $line =~ s/^JavaScript Statements/statements/;
    $line =~ s/^JavaScript Constants/constants/;
    $line =~ s/^JavaScript Properties/properties/;
    $line =~ s/^JavaScript Functions/functions/;
    $line =~ s/^JavaScript Methods/methods/;
    $line =~ s/^JavaScript Operators/operators/;
    $line =~ s/^JavaScript Objects/objects/;

    # Turn "Array/constructor Property (Array)" into Array/constructor
    # and "Array/concat Method (Array)" into Array/concat
    # etc.
    $line =~ s/\/([^ \/]+) Property \([^ ]+\)/\/$1/;
    $line =~ s/\/([^ \/]+) Method \([^ ]+\)/\/$1/;

    # Turn "Global/null Constant (JavaScript) " into "null"
    $line =~ s/^Global\/([^ \/]+) Constant \(JavaScript\) /$1 /;
    $line =~ s/^Global\/([^ \/]+) Constant /$1 /;

    # Turn "Global/decodeURI " into decodeURI
    $line =~ s/^Global\/([^ \/]+) /$1 /;

    # Turn /Array.isArray Function into /Array.isArray, etc
    $line =~ s/ Function / /;
    $line =~ s/ Property / /;
    $line =~ s/ Method / /;

    # Turn "Number/toLocaleString (Number)" into Number/toLocaleString
    $line =~ s/toLocaleString \([^ ]+\)/toLocaleString/;
    $line =~ s/Number\/Number Constants/Number\/Constants/;

    # Turn "Object/Object.defineProperties" into Object/defineProperties
    $line =~ s/\/Object\./\//;

    # Turn "RegExp/input (RegExp)" into "RegExp/input"
    $line =~ s/ \(RegExp\)//;

    # Turn "RegExp/$1...$9 Properties" into "RegExp/1 9 Properties"
    $line =~ s/RegExp\/\$1\.\.\.\$9 Properties/RegExp\/1 9 Properties/;

    # Turn "String/String.fromCharCode" into "String/fromCharCode"
    $line =~ s/String\.//;

    # Turn "JavaScript Operators/Bitwise NOT Operator (~)" to "operators/bitwise not"
    $line =~ s/JavaScript Operators\/([^\/]+) Operator \([^\/]+\)/operators\/$1/;

    # Turn "JavaScript Operators/void Operator " to "operators/void"
    $line =~ s/JavaScript Operators\/([^\/]+) Operator/operators\/$1/;

    if ($line =~ /^operators\//)
    {
        $line = lc ($line);
    }

    $line =~ s/division assignment \(\/=\)/division assignment/;
    $line =~ s/increment \(\+\+\) and decrement \(\-\-\)s/increment and decrement/;
    $line =~ s/division \(\/\)/division/;

    $line =~ s/conditional \(ternary\)/conditional ternary/;

    $line =~ s/do\.\.\.while/do while/;
    $line =~ s/for\.\.\.in/for in/;
    $line =~ s/if\.\.\.else/if else/;
    $line =~ s/try\.\.\.catch\.\.\.finally/try catch finally/;

    $line =~ s/ \(Regular Expression\)//;

    $line =~ s/JavaScript Future Reserved Words/future reserved words/;
    $line =~ s/JavaScript Reserved Words/reserved words/;

    $line =~ s/ \(JavaScript\)//;

    $line =~ s/operator \([^ ]+\)//;
    $line =~ s/increment \(\+\+\) and decrement \(\-\-\) operators/increment and decrement/;


    $line =~ s/Array\.isArray/isArray/;
    $line =~ s/0\.\.\.n Properties \(arguments\)/0 n Properties/;
    $line =~ s/Date\.//;
    $line =~ s/operators\/(.+) operator/operators\/$1/;
    $line =~ s/operators\/comparisons/operators\/comparison/;
    $line =~ s/compound assignments/compound assignment/;

    $line =~ s/ Statement//;

    if ($line ne "")
    {
        print "$line\n";
    }
} `cat OUTPUT.txt`;
