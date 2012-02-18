#!/usr/bin/env python
import urllib2

def get_amazon_query_url(query_params,access_key):
    #Prepare query
    serviceUrl = "http://ecs.amazonaws.com/onca/xml?"
    params = {}
    params["Service"]   = "AWSECommerceService"    
    params["AWSAccessKeyId"] = access_key
    params["Version"] = "2008-08-19"
    for p in query_params:
        params[p] = query_params[p]
    queryUrl = serviceUrl + "&".join([p+"="+params[p] for p in params])
    return queryUrl
    

def perform_amazon_query(query_params,access_key):    
    queryUrl = get_amazon_query_url(query_params,access_key)    
    #Perform query
    sock = urllib2.urlopen(queryUrl)
    xml = sock.read()    
    return xml