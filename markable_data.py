"""
This module parses the markable layer of a KAF/NAF object
"""

from span_data import *
from external_references_data import *
from lxml import etree


class Cmarkable:
    """
    This class encapsulates a <markable> NAF or KAF object
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
            self.node = etree.Element('markable')
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
        Returns the term identifier
        @rtype: string
        @return: the term identifier
        """
        if self.type == 'NAF':
            return self.node.get('id')
        elif self.type == 'KAF':
            return self.node.get('mid')
    
    def set_id(self,i):
        """
        Sets the identifier for the term
        @type i: string
        @param i: lemma identifier
        """
        if self.type == 'NAF':
            self.node.set('id',i)
        elif self.type == 'KAF':
            self.node.set('mid',i)
                    
    def get_lemma(self):
        """
        Returns the lemma of the object
        @rtype: string
        @return: the markable lemma
        """
        return self.node.get('lemma')
    
    def set_lemma(self,l):
        """
        Sets the lemma for the markable
        @type l: string
        @param l: lemma 
        """
        self.node.set('lemma',l)
        
            
    def get_source(self):
        """
        Returns the source attribute of the markable
        @rtype: string
        @return: the source of the markable feature
        """
        return self.node.get('source')

   
    def set_source(self,s):
        """
        Sets the source attribute
        @type s: string
        @param s: the source value
        """
        self.node.set('source',s)
        
    def get_span(self):
        """
        Returns the span object of the markable
        @rtype: L{Cspan}
        @return: the markable span
        """
        node_span = self.node.find('span')
        if node_span is not None:
            return Cspan(node_span)
        else:
            return None
        
    def set_span(self,this_span):
        """
        Sets the span for the markable
        @type this_span: L{Cspan}
        @param this_span: markable identifier
        """
        self.node.append(this_span.get_node())
                
        
    def add_external_reference(self,ext_ref):
        """
        Adds an external reference object to the markable
        @type ext_ref: L{CexternalReference}
        @param ext_ref: an external reference object
        """
        ext_refs_node = self.node.find('externalReferences')
        if ext_refs_node is None:
            ext_refs_obj = CexternalReferences()
            self.node.append(ext_refs_obj.get_node())
        else:
            ext_refs_obj = CexternalReferences(ext_refs_node)
            
        ext_refs_obj.add_external_reference(ext_ref)
        
        
    def get_external_references(self):
        """
        Iterator that returns all the external references of the markable
        @rtype: L{CexternalReference}
        @return: the external references
        """
        for ext_ref_node in self.node.findall('externalReferences'):
            ext_refs_obj = CexternalReferences(ext_ref_node)
            for ref in ext_refs_obj:
                yield ref
            
           
        
    
class Cmarkables:
    """
    This class encapsulates the term layer (collection of term objects)
    """
    def __init__(self,node=None,type='NAF'):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        @type type: string
        @param type: the type of the object (KAF or NAF)
        """
        self.idx = {}
        self.type = type
        if node is None:
            self.node = etree.Element('markables')
        else:
            self.node = node
            for node_markable in self.__get_node_markables():
                markable_obj = Cmarkable(node_markable,self.type)
                self.idx[markable_obj.get_id()] = node_markable    
    
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
    
    def to_kaf(self):
        """
        Converts the object to KAF (if it is NAF)
        """
        if self.type == 'NAF':
            self.type = 'KAF'
            for node in self.__get_node_terms():
                node.set('mid',node.get('id'))
                del node.attrib['id']

    def to_naf(self):
        """
        Converts the object to NAF (if it is KAF)
        """
        if self.type == 'KAF':
            self.type = 'NAF'
            for node in self.__get_node_terms():
                node.set('id',node.get('mid'))
                del node.attrib['mid']
                
    def __get_node_markables(self):
        for node_markable in self.node.findall('markable'):
            yield node_markable
            
    def __iter__(self):
        """
        Iterator that returns single markable objects in the layer
        @rtype: L{Cmarkable}
        @return: markable objects
        """
        for node_markable in self.__get_node_markables():
            yield Cmarkable(node_markable,self.type)
            
    def get_markable(self,mark_id):
        """
        Returns the markable object for the supplied identifier
        @type mark_id: string
        @param mark_id: term identifier
        """
        if mark_id in self.idx:
            return Cmarkable(self.idx[markable_id],self.type)
        else:
            return None
        
    def add_markable(self,markable_obj):
        """
        Adds a markable object to the layer
        @type markable_obj: L{Cmarkable}
        @param markable_obj: the markable object
        """
        self.node.append(markable_obj.get_node())
           
    def add_external_reference(self,markable_id, external_ref):
        """
        Adds an external reference for the given markable
        @type markable_id: string
        @param markable_id: the markable identifier
        @type external_ref: L{CexternalReference}
        @param external_ref: the external reference object
        """
        if markable_id in self.idx:
            markable_obj = Cterm(self.idx[markable_id],self.type)
            markable_obj.add_external_reference(external_ref)
        else:
            print markable_id,' not in self.idx'

    def remove_markables(self,list_mark_ids):
        """
        Removes a list of markables from the layer
        @type list_term_ids: list
        @param list_term_ids: list of markable identifiers to be removed  
        """
        nodes_to_remove = set()
        for markable in self:
            if markable.get_id() in list_mark_ids:
                nodes_to_remove.add(markable.get_node())
                #For removing the previous comment
                prv = markable.get_node().getprevious()
                if prv is not None:
                    nodes_to_remove.add(prv)
        
        for node in nodes_to_remove:
            self.node.remove(node)
        
