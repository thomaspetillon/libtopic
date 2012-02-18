#Topic ws module
#Provide web service client functionalities
import urllib2
from libtopic import xml

def callService(serviceUrl,params={}):
    #Prepare query
    if len(params)>0:
        queryUrl = serviceUrl + "?" + "&".join([p+"="+str(params[p]) for p in params])
    else:
        queryUrl = serviceUrl
    #Perform query
    try:
        sock = urllib2.urlopen(queryUrl)
        xml = sock.read()    
        return xml
    except:        
        raise CallServiceError(queryUrl)
        raise
class CallServiceError:
    def __init__(self,queryUrl):
        self.queryUrl = queryUrl        
    def __str__(self):
        return self.queryUrl

