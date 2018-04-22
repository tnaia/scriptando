#! /usr/bin/python

# Basic use (requires `graphviz`'s program `dot`:
# If `~/path/to/folder/` contains the texfiles,
# and you want an image called `tex-inclusion.png`,
# you should run
#
# python tex-inclusion-digraph.py ~/path/to/folder/ > dot -Tpng -o tex-inclusion.png
#
# Note: This will put the image in the current folder!
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

mypath = sys.argv[1]
print("// mypath is", mypath)
      
texfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f[-4:] == '.tex']

print("digraph texinclusion{")
for f in texfiles:
    fin = open(join(mypath,f))
    f_clean = f #was f.replace('-','_').replace('.','_')[:-4]
    for linum,l in enumerate(fin):
        m = includes_file(l)
        if m:
            included_file = m.group(2) #was m.group(2).replace('-','_').replace('.','_').replace('/','7')
            print ('    %40s -> "%s:%d"; // %s' % ('"'+f_clean+'"', included_file, linum, m.group(0)))
print("}")
