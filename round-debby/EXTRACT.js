#! /usr/bin/env rhino

var urlPrefix = "http://msdn.microsoft.com";
var url = "/en-us/library/ie/yek4tbz0%28v=vs.94%29.aspx?toc=1";
var skipPages = {"Get started": true, "Plan": true, "Develop": true};

function writeDump (parent, url)
{
    var completeUrl = urlPrefix + url;
    // print (">> Reading url " + completeUrl);
    var page = JSON.parse (readUrl (completeUrl));

    // Calculate prefix
    for (var index in page)
    {
        var item = page[index];
        if (item.Title in skipPages)
        {
            continue;
        }

        var fullPage = parent;
        if (parent != "")
        {
            fullPage += "/"
        }
        fullPage += item.Title;

        print (fullPage + " | " + item.Href);

        // See if there is a subtree of information
        if (item.ExtendedAttributes["data-tochassubtree"] == "true")
        {
            // Recurse to the subtree
            writeDump (fullPage, item.Href + "?toc=1");
        }
    }
}

// Start with top-level url and zero indentation
writeDump ("", url);
