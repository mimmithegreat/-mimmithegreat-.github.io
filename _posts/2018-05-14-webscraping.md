---
layout: post
title: webscraping
---

# Homework webscrapping

## Update:

Disclaimer: It took longer than expected because of my typical error, i.e. using [] instead of () for grouping, and not using
grouping at all.

But now it´s working.

So first: I put the Quellcode into the atom editor. I searched with the following regular expression: 
*(text.*(2006.05.\d\d\d\d))*

I copied all the findings into a new file called homework2.txt
in this file I added the missing url part.
The first () is of course so I can later use $1 with replacing:
*http://www.perseus.tufts.edu/hopper/dl$1*

this got me all the needed finished url.

The teacher explained to us in the last course unit how to get the missing url part: (xml-link on persheus)

I opend power shell and put in the command:

*.\wget -i homework2.txt -P -c subfolder*

wget without .\ won´t work!!!

After 15 Minutes or so it was finished and all the files are now in the subfolder -c 
I cannot open the files, however.

Note: wget.exe was in the same folder as homework2.txt
