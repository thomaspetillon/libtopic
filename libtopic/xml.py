#Topic xml module
#Provide xml utilities
#!/usr/bin/env python
import libxml2

class DynamicContainer:
# Dynamic container  
    def __init__(self,xmlNode):
        print 'DynamicContainer initialisation : ' + xmlNode.name
        # Initialize attributes
        attr = xmlNode.properties        
        while(attr != None) :            
            self.__dict__[attr.name] = attr.content
            print '     ' + attr.name + ': ' + attr.content 
            attr = attr.get_next()        
        # Initialize collections
        collectionNode = xmlNode.children        
        while(collectionNode != None):
            print "Processing : " +collectionNode.name            
            if collectionNode.properties:
                self.__dict__[collectionNode.name] = DynamicContainer(collectionNode)
                print xmlNode.name + "->" + collectionNode.name + " is set"
            else :
                collection = []
                collectionItem = collectionNode.children
                while (collectionItem != None):
                    collection.append(DynamicContainer(collectionItem))
                    collectionItem = collectionItem.next
                if (len(collection) > 0):
                    self.__dict__[collectionNode.name] = collection
            collectionNode = collectionNode.next
            
class ObjectNotFound:
    def __init__(self,xPathQuery):
        self.xPathQuery = xPathQuery        
    def __str__(self):
        return self.xPathQuery


def performXPathQuery(xml,xPathQuery):
    doc = libxml2.parseDoc(xml)
    ctxt = doc.xpathNewContext()
    output = ctxt.xpathEval(xPathQuery)
    return output   

    
def getList(xml,xPathQuery):    
    nodes = performXPathQuery(xml,xPathQuery)
    result = []
    for node in nodes:
        element = DynamicContainer(node)        
        result.append(element)
    return result

def getObject(xml,xPathQuery):
    nodes = performXPathQuery(xml,xPathQuery)
    if (len(nodes)==1):
        node = nodes[0]    
        return DynamicContainer(node)
    else:
        raise ObjectNotFound(xPathQuery)
        
def getAttributes(xmlnode):
    dict = {}
    for property in xmlnode.properties:
        if property.type=="attribute":
            dict[property.name] = property.content
    return dict

def hasAttribute(xmlnode,attribute_name):
    if not xmlnode.properties:
        return False
    return getAttributes(xmlnode).keys().__contains__(attribute_name)