#-*- coding: utf-8 -*- 
#!/usr/bin/env python

'''
Makes an url from an name
'''
def make_url(name):        
    # Remove accentued chars
    name = name.replace(u'\xe4','a')    # ä
    name = name.replace(u'\xe9','e')    # é
    name = name.replace(u'\xc9','e')    # E accent aigu
    name = name.replace(u'\xc8','e')    # E accent grave
    name = name.replace(u'\xca','e')    # E accent circonflexe
    name = name.replace(u'\xcb','e')    # E tréma
    name = name.replace(u'\xe8','e')    # è
    name = name.replace(u'\xea','e')    # ê
    name = name.replace(u'\xeb','e')    # ë
    name = name.replace(u'\xef','i')    # ï
    name = name.replace(u'\xe0','a')    # à
    name = name.replace(u'\xe1','a')    # a accent aigu
    name = name.replace(u'\xe2','a')    # â
    name = name.replace(u'\xe7','c')    # ç
    name = name.replace(u'\xfb','u')    # û
    name = name.replace(u'\xfc','u')    # ü
    name = name.replace(u'\xf6','o')    # ö
    name = name.replace(u'\xf4','o')    # ô
    name = name.replace(u'\x9c','oe')   # œ    
    name = name.replace(u'\xb0','o-')   # °
    name = name.replace(u'\xb4','-')    # guillemet simple oblique
    name = name.replace(u'\x91','-')    # guillemet simple oblique    
    name = name.replace(u'\x92','-')    # guillemet simple oblique    
    name = name.replace(u'\x93','-')    # guillemet double oblique 
    name = name.replace(u'\x94','-')    # guillemet double oblique
    name = name.replace(u'\xab','-')    # guillemet double oblique (ouvrant)
    name = name.replace(u'\xbb','-')    # guillemet double oblique (fermant)        
    name = name.replace(',','-')    
    name = name.replace('(','-')
    name = name.replace(')','-')
    name = name.replace("'",'-')
    name = name.replace('#','sharp')
    name = name.replace('&','-')
    name = name.replace('/','-')
    name = name.replace(' ','-')
    name = name.replace('.','-')    
    name = name.replace('"','-')
    name = name.replace('___','-')
    name = name.replace('__','-')
    name = name.replace('---','-')
    name = name.replace('--','-')
    name = name.strip('-')
    # Make lowercase
    return name.lower().replace(' ','')
