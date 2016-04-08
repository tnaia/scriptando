#!/bin/python
# -*- coding: utf-8 -*-

# Breaks lines longer than 50 characters,
# **except** those starting by a '>' (greater sign).
#
# Copyright 2016 Tássio Naia
#
# This is free software, licensed under GPL v3 or later.

import sys

filename = sys.argv[-1]
fin = open(filename)

max_len = 50

for line in fin:
    l = line.rstrip()
    if l[0] == '>':
        print(l)
    else:
        line_len = len(l)
        index = 0
        while line_len -index > max_len:
            print(l[index:index+max_len])
            index += max_len
        if index < line_len:
            print(l[index:])

fin.close()
