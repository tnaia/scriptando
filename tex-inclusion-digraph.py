#! /usr/bin/python
# Files included by each tex file.
# tns@polignu.org

# Basic use (requires `graphviz`'s program `dot`:
# If `~/path/to/folder/` contains the texfiles,
# and you want an image called `tex-inclusion.png`,
# you should run
#
# python tex-inclusion-digraph.py ~/path/to/folder/ | dot -Tpng -o tex-inclusion.png
#
# Note: This will put the image in the current folder!

# Increase whenever this file is changed!
version="0.5"

# CHANGELOG
# - v0.5 node names can contain double quotes!
# - v0.4 error message if wrong number of argumenst
# - v0.3 edges have line numbers
# - v0.2 node names can contain anything but double quotes
# - v0.1 it's alive!


from os import listdir
from os.path import isfile, join
import os
import re
import sys


# I am looking for occurences of
# - \input{X}
# - \include{X}
# - \includegraphics{X}
# - \bibliographystyle{X}
# - \bibliography{X}

def includes_file(line):
    p = re.compile('\\\\(include|input|bibliography)[^\{]*\{([^\}]+)\}')
    return p.search(line)

if len(sys.argv) != 2:
    print("Check which texfiles in a folder include other files.\nVersion " + version)
    print("Usage: texinclusion <PATH>\n" % sys.argv[0])
    exit(1)
    
mypath = sys.argv[1]
print("// mypath is", mypath)

work_dir = os.getcwd()
wd_len = len(work_dir)
texfiles = [(dp,f) for dp, dn, fn in os.walk(os.path.expanduser(mypath))
       for f in fn if ('/.git/' not in os.path.join(dp,f) and f[-4:]=='.tex')]

#  [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser("~/work/visconde/")) for f in fn if ('/.git/' not in os.path.join(dp,f) and )]


print("digraph texinclusion{")
for (dp,f) in texfiles:
    fin = open(os.path.join(dp,f))
    f_clean = f.replace('"','\\"')
    dp_clean = dp[wd_len:]
    for linum,l in enumerate(fin):
        m = includes_file(l)
        if m:
            included_file = m.group(2)
            print ('    %40s -> "%s" [label="%d"]; // %s' % ('"'+os.path.join(dp,f_clean)+'"', os.path.join(dp,included_file), linum, m.group(0)))
print("}")
