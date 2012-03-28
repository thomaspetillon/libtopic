#-*- coding: utf-8 -*- 
#!/usr/bin/env python

def html_unescape(s):
    return s.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#39;',"'").replace("%20"," ")
    
def get_safe_html(input):
    input = input.replace(u'\xe9',"&eacute;")
    input = input.replace(u'\xe8',"&egrave;")
    input = input.replace(u'\xe0',"&agrave;")
    input = input.replace(u'\xe2',"&acirc;")
    input = input.replace(u'\xf4',"&ocirc;")
    input = input.replace(u'\xc9',"&Eacute;")
    input = input.replace(u'\xef',"&iuml;")
    input = input.replace(u'\xb0','&deg;')    # °    	
    return input
