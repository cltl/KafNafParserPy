"""
This module implements a parser for the coreference layer in KAF/NAF
"""

from lxml import etree
from span_data import Cspan

class Ccoreference:
    """
    This class encapsulates a coreference object in KAF/NAF
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
            self.node = etree.Element('coref')
        else:
            self.node = node
            
    def get_id(self):
        """
        Returns the identifier of the object
        @rtype: string
        @return: identifier of the corefence object
        """
        if self.type == 'NAF':
            return self.node.get('id')
        elif self.type == 'KAF':
            return self.node.get('coid')
        
    
    def get_type(self):
        """
        Returns the type of the coreference object
        @rtype: string
        @return: type of the corefence object
        """
        if self.type == 'NAF':
            return self.node.get('type')
    
    def get_spans(self):
        """
        Iterator that returns all the span objects of the corerefence
        @rtype: L{Cspan}
        @return: list of span objects for the coreference object
        """
        for node_span in self.node.findall('span'):
            yield Cspan(node_span)
            
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
            

class Ccoreferences:
    """
    This class encapsulates the coreference layer (a set of coreference objects)
    """

    def __init__(self,node=None, type='NAF'):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        @type type: string
        @param type: the type of the object (KAF or NAF)
        """
        self.type = type
        if node is None:
            self.node = etree.Element('coreferences')
        else:
            self.node = node
            
    def __get_corefs_nodes(self):
        for coref_node in self.node.findall('coref'):
            yield coref_node
            
    def get_corefs(self):
        """
        Iterator that returns all the coreference objects
        @rtype: L{Ccoreference}
        @return: list of coreference objects (iterator)
        """
        for coref_node in self.__get_corefs_nodes():
            yield Ccoreference(coref_node,self.type)
            
    def to_kaf(self):
        """
        Converts the coreference layer to KAF
        """
        if self.type == 'NAF':
            for node_coref in self.__get_corefs_nodes():
                node_coref.set('coid',node_coref.get('id'))
                del node_coref.attrib['id']
        
    def to_naf(self):
        """
        Converts the coreference layer to NAF
        """
        if self.type == 'KAF':
            for node_coref in self.__get_corefs_nodes():
                node_coref.set('id',node_coref.get('coid'))
                del node_coref.attrib['coid']
                    
            