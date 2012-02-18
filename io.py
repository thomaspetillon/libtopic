#!/usr/bin/env python
import os

def get_lines_from_file(path):
    f = open(path,"r")
    s = f.read()
    f.close()
    lines = s.split("\n")
    return lines

def create_directory(dir):
    os.makedirs(dir)