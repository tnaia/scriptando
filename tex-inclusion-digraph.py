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
      
texfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f[-4:] == '.tex']

print("digraph texinclusion{")
for f in texfiles:
    fin = open(join(mypath,f))
    f_clean = f.replace('"','\\"')
    for linum,l in enumerate(fin):
        m = includes_file(l)
        if m:
            included_file = m.group(2)
            print ('    %40s -> "%s" [label="%d"]; // %s' % ('"'+f_clean+'"', included_file, linum, m.group(0)))
print("}")
