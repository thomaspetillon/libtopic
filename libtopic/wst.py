#Topic wst module (Web Service Templates)
#Provide web service server functionalities, based on templates

#!/usr/bin/env python
import sys
import libxml2
import django.utils.html
from libtopic.xml import performXPathQuery
from libtopic.xml import getAttributes
from libtopic.xml import hasAttribute
from libtopic.lists import get_distinct_list
from libtopic.lists import flatten_list

def get_first_child(node):
    result = node.children        
    while result and result.type == "text":
        result = result.next
    return result
    
def get_next_sibling(node):
    result = node.next
    while result and result.type == "text":
        result = result.next
    return result    
    
class WsTemplate:    
    def __init__(self,dir,service_name):
        # Load XML template from file
        file_path = dir+"/"+service_name+".xml"
        f = open(file_path, "r")
        self.xml= f.read()
        self.xml = self.xml.replace('\t','')
        self.xml = self.xml.replace('\n','')
        f.close()
        # Parse XML
        parameters = performXPathQuery(self.xml,'/WsTemplate/Parameters')
        nodes      = performXPathQuery(self.xml,'/WsTemplate')        
        if len(parameters)==1:
            self.parameter_node = parameters[0]
            self.root_node      = get_next_sibling(get_first_child(nodes[0]))
        else:            
            self.root_node      = get_first_child(nodes[0])
            
    def serialize_field(self,instance,field_node,output_node):
        print "Serializing field : '" + str(field_node.name) + "'"        
        val = getattr(instance,field_node.name)
        if val:
            prop_val = unicode(val).encode("utf-8")
            if len(prop_val)>0:
                if hasAttribute(field_node,'html_encode'):
                    html_encode = getAttributes(field_node)['html_encode']
                    if html_encode == "True":
                        prop_val = django.utils.html.escape(prop_val) 
                output_node.setProp(field_node.name, prop_val)
        
    def serialize_node(self,node,instance,output_node):
        print "Serializing node : '" + str(node) + "'"        
        # Without children : serialize node as attribute of parent instance
        # With children, loop on each child and make recursive call to serialize node                
        if get_first_child(node):            
            output_child_node = output_node.addChild(libxml2.newNode(node.name)) 
            current_node = get_first_child(node)
            while current_node:                
                if hasAttribute(current_node,'model'):
                    self.serialize_collection(current_node,output_child_node,instance)
                else:
                    if get_first_child(current_node):                    
                        recursive_instance = getattr(instance,current_node.name)
                        self.serialize_node(current_node,recursive_instance,output_child_node)
                        pass
                    else:
                        self.serialize_field(instance,current_node,output_child_node)
                        pass
                current_node = get_next_sibling(current_node)
        else:
            self.serialize_field(instance,node,output_node)            
            
    def serialize_collection(self,collection_node,output_parent_node,parent_instance):
        #print "Serializing a collection : '" + str(collection_node) + "'"        
        # First, load the collection
        results = self.load_collection(collection_node,parent_instance)
        if len(results)==0:
            return
        output_collection_node = output_parent_node.addChild(libxml2.newNode(collection_node.name))        
        instance_node = get_first_child(collection_node)
        # Then, serialize each instance
        for obj in results:
            self.serialize_node(instance_node,obj,output_collection_node)
            
    def evaluate_parameters(self,str):
        for key in self.parameters.keys():
            str = str.replace(key,self.parameters[key])
        return str
                      
    def load_collection_from_filters(self,collection_node,parent_instance,models,class_name):
        # Construct filters
        filters_str = getAttributes(collection_node)['filters']        
        filters     = filters_str.split('|')
        args = {}
        for filter in filters:
            tokens = filter.split('=')
            filter_by = tokens[0]
            filter_value = tokens[1]
            # Evaluate parameters
            filter_value = self.evaluate_parameters(filter_value)            
            args[filter_by]=filter_value        
        # Perform query
        if hasAttribute(collection_node,"order_by"):
            order_by = getAttributes(collection_node)['order_by']            
            return getattr(models,class_name).objects.filter(**args).order_by(*order_by.split("|"))
        else:            
            return getattr(models,class_name).objects.filter(**args)
        
    def evaluate_import_directive(self,import_directive):
        print "Evaluating import directive :" + import_directive 
        tokens = import_directive.split('|')
        module_name = tokens[0]
        result = "import "+module_name
        if len(tokens)>1:        
            class_name  = tokens[1]
            result = "from " + module_name + " import "+class_name
        return result
        
    def load_collection_from_source(self,collection_node,parent_instance,models,class_name):
        print 'Entering load_collection_from_source'
        source = getAttributes(collection_node)['source']
        if parent_instance:
            source = source.replace('@parentid',str(getattr(parent_instance,"id")))
        source = self.evaluate_parameters(source).encode("utf-8")        
        # Import additionnal classes, if specified
        import_directives = []
        imports = ""
        if hasAttribute(collection_node,'import'):
            import_str = getAttributes(collection_node)['import']
            import_tokens = import_str.split(',')            
            for import_token in import_tokens:
                import_directives.append(self.evaluate_import_directive(import_token))
            imports ="\n".join(import_directives)
            imports += '\n'        
        # Execute code        
        source = "results="+source
        source = imports + source
        print "Compiling : " + source
        byte_code = compile(source,"compilation_errors.txt","exec")        
        exec(byte_code)        
        print 'Loaded collection. Number of elements :'+str(len(results))
        return results
        
    def load_collection(self,collection_node,parent_instance):
        # Dynamically load instance
        model = getAttributes(collection_node)['model']
        tokens = model.split('.')
        module_name = ".".join(tokens[:len(tokens)-1])
        class_name  = tokens[len(tokens)-1:][0]
        models = __import__(module_name,globals(),locals(),[class_name],-1)
        # Load collection (from filters or from source)
        if hasAttribute(collection_node,'filters'):            
            return self.load_collection_from_filters(collection_node,parent_instance,models,class_name)
        else:
            source = getAttributes(collection_node)['source']
            return self.load_collection_from_source(collection_node,parent_instance,models,class_name)
    
    def eval(self,parameters={}):
        self.parameters = parameters
        doc = libxml2.parseDoc(u"<output/>")
        self.serialize_collection(self.root_node,doc.getRootElement(),None)
        return doc
    
        
        
