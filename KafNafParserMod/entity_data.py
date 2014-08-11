"""
Parser for the entity layer in KAF/NAF
"""

## Modified for KAF NAF adaptation
from lxml import etree
from lxml.objectify import dump
from references_data import *
    
    
class Centity:
    """
    This class encapsulates the entity element in KAF/NAF
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
            self.node = etree.Element('entity')
        else:
            self.node = node

    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.noce
                    
    def get_id(self):
        """
        Returns the identifier of the element
        @rtype: string
        @return: the identifier of the entity
        """
        if self.type == 'NAF':
            return self.node.get('id')
        elif self.type == 'KAF':
            return self.node.get('eid')
    
    def get_type(self):
        """
        Returns the type of the entity
        @rtype: string
        @return: the type of the entity
        """
        return self.node.get('type')
    
    def get_references(self):
        """
        Returns the references of the entity
        @rtype: L{Creferences}
        @return: list of references (iterator)
        """
        for ref_node in self.node.findall('references'):
            yield Creferences(ref_node)
    
    
    
class Centities:
    """
    This class encapsulates the entity layer in KAF/NAF
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
            self.node = etree.Element('entities')
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
        Converts the layer from KAF to NAF
        """
        if self.type == 'NAF':
            for node in self.__get_entity_nodes():
                node.set('eid',node.get('id'))
                del node.attrib['id']

    def to_naf(self):
        """
        Converts the layer from NAF to KAF
        """
        if self.type == 'KAF':
            for node in self.__get_entity_nodes():
                node.set('id',node.get('eid'))
                del node.attrib['eid']
                
    def __get_entity_nodes(self):
        for ent_node in self.node.findall('entity'):
            yield ent_node
                
    def __iter__(self):
        """
        Iterator that returns the entities of the layer
        @rtype: L{Centity}
        @return: list of entities (iterator)
        """
        for ent_node in self.__get_entity_nodes():
            yield Centity(ent_node,self.type)
        
        
    def __str__(self):
        return dump(self.node)
