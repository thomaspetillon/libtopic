#!/usr/bin/env python
import urllib2
from libtopic import regex

def remove_trailing_slash(url):
    if url.endswith('/'): # Removing trailing '/' if any
        url = url[0:len(url)-1]
    return url

def get_links_helper(root_url,url,results):
    url = remove_trailing_slash(url)
    if url in results:
        return # Already analyzed
    print 'Analysing url : ' + url
    results.append(url)
    sock = urllib2.urlopen(url)
    html = sock.read()
    pattern = "href=\"[^\"]+"
    links = [r.text for r in regex.find_all_matches(html,pattern)]
    for link in links:        
        if link.startswith("href=\"/"):            
            link_to_follow = link[6:]            
            url2 = root_url + link_to_follow            
            # Make recursive call
            get_links_helper(root_url,url2,results)
    return results

def get_links(root_url):
    results = []    
    return get_links_helper(root_url,root_url,results)
    