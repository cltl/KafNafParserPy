"""
Parser for the feature layer in KAF/NAF
"""

from .references_data import *



class Cproperty:
    """
    This class encapsulates the property element in KAF/NAF
    """
    def __init__(self,node=None,type='NAF'):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        @type type: string
        @param type: the type of the object (KAF or NAF)
        """
        self.type = type
        if node is None:
            self.node = etree.Element('property')
        else:
            self.node = node
    
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
    
    def get_id(self):
        """
        Returns the identifier of the element
        @rtype: string
        @return: the identifier of the element
        """
        if self.type == 'KAF':
            return self.node.get('pid')
        elif self.type == 'NAF':
            return self.node.get('id')
  
    def set_id(self,pid):
        """
        Set the property identifier
        @type pid: string
        @param pid: property identifier 
        """
        if self.type == 'KAF':
            return self.node.set('pid',pid)
        elif self.type == 'NAF':
            return self.node.set('id',pid)
          
    def get_type(self):
        """
        Returns the type of the property
        @rtype: string
        @return: the type of the element
        """
        return self.node.get('lemma')

    def set_type(self,t):
        """
        Set the property type
        @type t: string
        @param t: property type 
        """
        return self.node.set('lemma',t)
    
    def get_references(self):
        """
        Returns the references of the element
        @rtype: L{Creferences}
        @return: the references object of the element (iterator)
        """
        for ref_node in self.node.findall('references'):
            yield Creferences(ref_node)
            
    def set_reference(self,ref):
        """
        Set the property references
        @type ref: L{Creferences}
        @param ref: property references 
        """
        self.node.append(ref.get_node())
                             
                        
                
class Cproperties:
    """
    This class encapsulates the property layer in KAF/NAF
    """
    def __init__(self,node=None,type='NAF'):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        @type type: string
        @param type: the type of the object (KAF or NAF)
        """
        self.type=type
        if node is None:
            self.node = etree.Element('properties')
        else:
            self.node = node
            
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
            
    def __iter__(self):
        """
        Iterator that returns all the properties
        @rtype: L{Cproperty}
        @return: list of properties (iterator)
        """
        for prop_node in self.node.findall('property'):
            yield Cproperty(prop_node,self.type)
            
    def add_property(self,pid, label,term_span):
        """
        Adds a new property to the property layer
        @type pid: string
        @param pid: property identifier
        @type label: string
        @param label: the label of the property
        @type term_span: list
        @param term_span: list of term identifiers
        """
        new_property = Cproperty(type=self.type)
        self.node.append(new_property.get_node())
        ##Set the id
        if pid is None:
            ##Generate a new pid
            existing_pids = [property.get_id() for property in self]
            n = 0
            new_pid = ''
            while True:
                new_pid = 'p'+str(n)
                if new_pid not in existing_pids: break
                n += 1
            pid = new_pid
        new_property.set_id(pid)
        
        new_property.set_type(label)
        
        new_ref = Creferences()
        new_ref.add_span(term_span)
        new_property.set_reference(new_ref)
 
        
                
class Cfeatures:
    """
    This class encapsulates the features layer in KAF/NAF
    """
    def __init__(self,node=None,type='NAF'):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        @type type: string
        @param type: the type of the object (KAF or NAF)
        """
        self.type = type
        if node is None:
            self.node = etree.Element('features')
        else:
            self.node = node
        
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
    
    def to_kaf(self):
        """
        Converts the element to NAF
        """
        if self.type == 'NAF':
            ##convert all the properties
            for node in self.node.findall('properties/property'):
                node.set('pid',node.get('id'))
                del node.attrib['id']

    def to_naf(self):
        """
        Converts the element to KAF
        """
        if self.type == 'KAF':
            ##convert all the properties
            for node in self.node.findall('properties/property'):
                node.set('id',node.get('pid'))
                del node.attrib['pid']                
            
    def add_property(self,pid, label,term_span):
        """
        Adds a new property to the property layer
        @type pid: string
        @param pid: property identifier
        @type label: string
        @param label: the label of the property
        @type term_span: list
        @param term_span: list of term identifiers
        """
        node_prop = self.node.find('properties')
        if node_prop is None:
            properties = Cproperties(type=self.type)
            self.node.append(properties.get_node())
        else:
            properties = Cproperties(node=node_prop,type=self.type)
            
        properties.add_property(pid, label,term_span)
        
        
    def get_properties(self):
        """
        Iterator that returns all the properties of the layuer
        @rtype: L{Cproperty}
        @return: list of property objects (iterator)
        """
        node_prop = self.node.find('properties')
        if node_prop is not None:
            obj_properties = Cproperties(node_prop,self.type)
            for prop in obj_properties:
                yield prop
                
                
    def remove_properties(self):
        """
        Removes the property layer, if exists
        """
        node_prop = self.node.find('properties')
        if node_prop is not None:
            self.node.remove(node_prop)
            