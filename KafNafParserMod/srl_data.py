"""
Parser for the semantic role labelling layer in KAF/NAF
"""

from span_data import *
from external_references_data import *
from lxml import etree

class Crole:
    """
    This class encapsulates a single role in the layer
    """
    def __init__(self,node):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        if node is None:
            self.node = etree.Element('role')
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
        return self.node.get('id')
    
    def get_sem_role(self):
        """
        Returns the semRole attribute of the element
        @rtype: string
        @return: the semRole of the element
        """
        return self.node.get('semRole')
    
    def get_external_references(self):
        """
        Returns the external references of the element
        @rtype: L{CexternalReference}
        @return: the external references (iterator)
        """
        node = self.node.find('externalReferences')
        if node is not None:
            ext_refs = CexternalReferences(node)
            for ext_ref in ext_refs:
                yield ext_ref
                
    def add_external_reference(self,ext_ref):
        """
        Adds an external reference to the role
        @param ext_ref: the external reference object
        @type ext_ref: L{CexternalReference}
        """
        #check if the externalreferences sublayer exist for the role, and create it in case
        node_ext_refs = self.node.find('externalReferences')
        ext_refs = None
        if node_ext_refs == None:
            ext_refs = CexternalReferences()
            self.node.append(ext_refs.get_node())
        else:
            ext_refs = CexternalReferences(node_ext_refs)
        
        ext_refs.add_external_reference(ext_ref)
        
    def get_span(self):
        """
        Returns the span of the role
        @rtype: L{Cspan}
        @return: the span object of the element
        """
        node = self.node.find('span')
        if node is not None:
            return Cspan(node)
        else:
            return None
    
class Cpredicate:
    def __init__(self,node):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        if node is None:
            self.node = etree.Element('predicate')
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
        return self.node.get('id')
    
    def get_uri(self):
        """
        Returns the URI of the element
        @rtype: string
        @return: the URI of the element
        """
        return self.node.get('uri')
    
    def get_confidence(self):
        """
        Returns the confidence of the element
        @rtype: string
        @return: the confidence of the element
        """
        return self.node.get('confidence')
        
    def get_span(self):
        """
        Returns the span object of the element
        @rtype: L{Cspan}
        @return: the span object of the element
        """
        node = self.node.find('span')
        if node is not None:
            return Cspan(node)
        else:
            return None
    
    def get_external_references(self):
        """
        Iterator to get the external references
        @rtype: L{CexternalReference}
        @return: iterator for external references
        """
        node = self.node.find('externalReferences')
        if node is not None:
            ext_refs = CexternalReferences(node)
            for ext_ref in ext_refs:
                yield ext_ref
                
    def get_roles(self):
        """
        Iterator to get the roles
        @rtype: L{Crole}
        @return: iterator for getting the role objects
        """
        for node_role in self.node.findall('role'):
            yield Crole(node_role)
            

class Csrl:
    """
    This class encapsulates the semantic role labelling layer
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
            self.node = etree.Element('srl')
        else:
            self.node = node
            
        # Create a mapping role id --> node
        self.map_roleid_node = {}
        for predicate in self.get_predicates():
            for role in predicate.get_roles():
                self.map_roleid_node[role.get_id()] = role.get_node()
                
            
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
    
    def get_predicates(self):
        """
        Iterator to get the roles
        @rtype: L{Cpredicate}
        @return: iterator for getting the predicate objects
        """
        for node_pre in self.node.findall('predicate'):
            yield Cpredicate(node_pre)
            
    def add_external_reference_to_role(self,role_id,ext_ref):
        """
        Adds an external reference to a role identifier
        @param role_id: the role identifier
        @type role_id: string
        @param ext_ref: the external reference
        @type ext_ref: L{CexternalReference}
        """
        node_role = self.map_roleid_node[role_id]
        obj_role = Crole(node_role)
        obj_role.add_external_reference(ext_ref)
            
            