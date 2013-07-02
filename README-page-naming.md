MSDN upload page naming plan
----

The converted wiki pages are ready for upload.  This communique describes how they
should be named.  The special file named "round-alice/upload-mapping.wiki" contains the
current mapping between the pages and where they are uploaded.

Currently, the top-level hierarchy is:
* Objects
* Constants
* Properties
* Functions
* Methods
* Operators
* Statements
* Directives
* Errors
* Reserved Words
* Future Reserved Words

Within each hierarchy are kinds of each, like kinds of Objects or kinds of Statements.

These pages listed below are not so much of a problem.  They can be organized into
subpages or incorporated into some subpage:
* "Directives" has a single directive subpage "use strict" which should not be used.
* "Errors" has two subpages: "Run time" and "Syntax".
* "Reserved Words" is a single page that lists words that are already used.
* "Future Reserved Words" is a single page that lists words that might be used.

These pages are the main problem:
* Objects
* Operators
* Statements

Each of these is described below.

Objects
----
If JavaScript had classes, the Objects hierarchy would represent it.  Instead,
JavaScript only has notable Objects used mostly to create new instances, such as
creating a new Array.  Special objects like "arguments" exist automatically inside a
function.  Other special objects are Function, Global, Object.

Subpages for the Array object, for example, describe each property, function, method, or
constant the Array object has:

* Array has three properties: constructor, length, and prototype.
* Array has one function: Array.isArray.
* Array has many methods: concat, every, filter, forEach, indexOf, join, lastIndexOf, map,
pop, push, reduce, reduceRight, reverse, shift, slice, some, sort, splice, toString,
unshift, and valueOf.
* Math has a constant Math.E.

The list of all notable Objects:

* ActiveXObject
* Array
* ArrayBuffer
* arguments
* Boolean
* DataView
* Date
* Debug
* Enumerator
* Error
* Float32Array
* Float64Array
* Function
* Global
* Int8Array
* Int16Array
* Int32Array
* JSON
* Math
* Number
* Object
* RegExp
* Regular Expression
* String
* Uint8Array
* Uint16Array
* Uint32Array
* VBArray
* WinRTError

Operators
----
The operators available are each their own page:

* Addition Assignment
* Addition
* Assignment
* Bitwise AND Assignment
* Bitwise AND
* Bitwise Left Shift
* Bitwise NOT
* Bitwise OR Assignment
* Bitwise OR
* Bitwise Right Shift
* Bitwise XOR Assignment
* Bitwise XOR
* Comma
* Comparison
* Compound Assignment
* Conditional Ternary
* delete
* Division Assignment
* Division
* in
* Increment and Decrement
* instanceof
* Left Shift Assignment
* Logical AND
* Logical NOT
* Logical OR
* Modulus Assignment
* Modulus
* Multiplication Assignment
* Multiplication
* new
* Right Shift Assignment
* Subtraction Assignment
* Subtraction
* typeof
* Unsigned Right Shift Assignment
* Unsigned Right Shift
* void

Statements
----
Statements each have their own page:

* break
* cc on
* Comment
* continue
* debugger
* do while
* for
* for in
* function
* if
* if else
* Labeled
* return
* set
* switch
* this
* throw
* try catch finally
* var
* while
* with
