#!/usr/bin/env python
import re

class regex_match:
    pass
    
def find_all_matches(input,pattern):
    result = []
    p = re.compile(pattern)    
    iter = p.finditer(input)
    for m in iter:
        match = regex_match()
        match.start = m.start()
        match.end   = m.end()
        match.text  = input[match.start:match.end]
        result.append(match)
    return result
    
def find_first(input,pattern):
    result = []
    p = re.compile(pattern)    
    match = p.search(input)
    if match:
        text  = input[match.start():match.end()]    
        return text
    else:
        return None

def is_match(input,pattern):
    result = []
    p = re.compile(pattern)    
    matches = p.findall(input)
    if (len(matches)>0):
        return True
    else:
        return False
    
def is_integer(str):
    try:
        test = int(str)
        return True
    except:
        return False
    
def is_phone_number(str):
    return is_match(str,"[0-9]{10}")
    
def is_valid_email(str):
    pattern = "[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,4}"    
    p = re.compile(pattern)    
    matches = p.findall(str)
    if (len(matches)==1):        
        if matches[0]==str:
            return True
    # In other cases, return False
    return False        
