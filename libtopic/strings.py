#!/usr/bin/env python

# Remove the portion between start & end
def remove_portion(input,start,end):
    left  = input[0:start]
    right = input[end+1:]
    result = left + right
    return result

def capitalize_first_letter(str):
    return str[:1].upper()+str[1:]
