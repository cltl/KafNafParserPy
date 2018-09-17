"""
This module implements a parser for the coreference layer in KAF/NAF
"""

from lxml import etree

from .external_references_data import CexternalReferences
from .span_data import Cspan

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
     
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
            
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
        
        
    def set_id(self, this_id):
        """
        Sets the identifier of the object
        @type: string
        @param: identifier of the corefence object
        """
        if self.type == 'NAF':
            return self.node.set('id', this_id)
        elif self.type == 'KAF':
            return self.node.set('coid', this_id)

    
    def get_type(self):
        """
        Returns the type of the coreference object
        @rtype: string
        @return: type of the corefence object
        """
        if self.type == 'NAF':
            return self.node.get('type')

    def set_type(self, this_type):
        """
        Sets the type of the coreference object
        @type: string
        @param: type of the corefence object
        """
        if self.type == 'NAF':
            return self.node.set('type', this_type) 
    
    def add_span(self,term_span):
        """
        Adds a list of term ids a new span in the references
        @type term_span: list
        @param term_span: list of term ids
        """
        new_span = Cspan()
        new_span.create_from_ids(term_span)
        self.node.append(new_span.get_node())

    def add_span_object(self, nafSpan):
        """
        Adds naf span object in the references
        @type term_span: list
        @param term_span: list of term ids
        """
        self.node.append(nafSpan.get_node())
        
    def remove_span(self,span):
        """
        Removes a specific span from the coref object
        """
        this_node = span.get_node()
        self.node.remove(this_node)
    
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

    def add_external_reference(self, ext_ref):
        """
        Adds an external reference to the coref element
        @param ext_ref: the external reference object
        @type ext_ref: L{CexternalReference}
        """
        # check if the externalreferences sublayer exist for the coref element, and create it in case
        node_ext_refs = self.node.find('externalReferences')
        ext_refs = None
        if node_ext_refs == None:
            ext_refs = CexternalReferences()
            self.node.append(ext_refs.get_node())
        else:
            ext_refs = CexternalReferences(node_ext_refs)

        ext_refs.add_external_reference(ext_ref)

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
    
    def add_coreference(self,coreference):
        self.node.append(coreference.get_node())        
            
    
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
            
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

    def __iter__(self):
        """
        Iterator that returns all the coreference objects
        @rtype: L{Ccoreference}
        @return: list of coreference objects (iterator)
        """
        return self.get_corefs()

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
    
    
    def remove_coreference(self,coid):
        """
        Removes the coreference with specific identifier
        @type coid: string
        @param coid: the coreference identifier
        """
        for this_node in self.node.findall('coref'):
            if this_node.get('id') == coid:
                self.node.remove(this_node)
                break
