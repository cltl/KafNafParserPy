"""
This module parses the term layer of a KAF/NAF object
"""

from span_data import *
from external_references_data import *
from term_sentiment_data import *
from lxml import etree


class Cterm:
    """
    This class encapsulates a <term> NAF or KAF object
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
            self.node = etree.Element('term')
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
            return self.node.get('tid')
    
    def set_id(self,i):
        """
        Sets the identifier for the term
        @type i: string
        @param i: lemma identifier
        """
        if self.type == 'NAF':
            self.node.set('id',i)
        elif self.type == 'KAF':
            self.node.set('tid',i)
                    
    def get_lemma(self):
        """
        Returns the lemma of the object
        @rtype: string
        @return: the term lemma
        """
        return self.node.get('lemma')
    
    def set_lemma(self,l):
        """
        Sets the lemma for the term
        @type l: string
        @param l: lemma 
        """
        self.node.set('lemma',l)
    
    def get_pos(self):
        """
        Returns the part-of-speech of the object
        @rtype: string
        @return: the term pos-tag
        """
        return self.node.get('pos')
 
    def set_pos(self,p):
        """
        Sets the postag for the term
        @type p: string
        @param p: pos-tag
        """
        self.node.set('pos',p)
        
           
    def set_type(self,t):
        """
        Sets the type for the lemma
        @type t: string
        @param t: type for the term
        """
        self.node.set('type',t)
        
            
    def get_morphofeat(self):
        """
        Returns the morphofeat attribute of the term
        @rtype: string
        @return: the term morphofeat feature
        """
        return self.node.get('morphofeat')

    def set_morphofeat(self,mf):
        """
        Sets the type for the lemma
        @type t: string
        @param t: type for the term
        """
        self.node.set('morphofeat',mf)
    
    def set_morphofeat(self,m):
        """
        Sets the morphofeat attribute
        @type m: string
        @param m: the morphofeat value
        """
        self.node.set('morphofeat',m)
        
    def get_span(self):
        """
        Returns the span object of the term
        @rtype: L{Cspan}
        @return: the term span
        """
        node_span = self.node.find('span')
        if node_span is not None:
            return Cspan(node_span)
        else:
            return None
        
    def set_span(self,this_span):
        """
        Sets the span for the lemma
        @type this_span: L{Cspan}
        @param this_span: lemma identifier
        """
        self.node.append(this_span.get_node())
        
    def get_sentiment(self):
        """
        Returns the sentiment object of the term
        @rtype: L{Cterm_sentiment}
        @return: the term sentiment
        """
        sent_node = self.node.find('sentiment')
        
        if sent_node is None:
            return None
        else:
            return Cterm_sentiment(sent_node)
        
        
    def add_external_reference(self,ext_ref):
        """
        Adds an external reference object to the term
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
        
    def add_term_sentiment(self,term_sentiment):
        """
        Adds a sentiment object to the term
        @type term_sentiment: L{Cterm_sentiment}
        @param term_sentiment: an external reference object
        """
        self.node.append(term_sentiment.get_node())
        
    def get_external_references(self):
        """
        Iterator that returns all the external references of the term
        @rtype: L{CexternalReference}
        @return: the external references
        """
        ext_ref_node = self.node.find('externalReferences')
        if ext_ref_node is not None:
            ext_refs_obj = CexternalReferences(ext_ref_node)
            for ref in ext_refs_obj:
                yield ref
            
           
        
    
class Cterms:
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
            self.node = etree.Element('terms')
        else:
            self.node = node
            for node_term in self.__get_node_terms():
                term_obj = Cterm(node_term,self.type)
                self.idx[term_obj.get_id()] = node_term    
    
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
                node.set('tid',node.get('id'))
                del node.attrib['id']

    def to_naf(self):
        """
        Converts the object to NAF (if it is KAF)
        """
        if self.type == 'KAF':
            self.type = 'NAF'
            for node in self.__get_node_terms():
                node.set('id',node.get('tid'))
                del node.attrib['tid']
                
    def __get_node_terms(self):
        for node_term in self.node.findall('term'):
            yield node_term
            
    def __iter__(self):
        """
        Iterator that returns single term objects in the layer
        @rtype: L{Cterm}
        @return: term objects
        """
        for node_term in self.__get_node_terms():
            yield Cterm(node_term,self.type)
            
    def get_term(self,term_id):
        """
        Returns the term object for the supplied identifier
        @type term_id: string
        @param term_id: term identifier
        """
        if term_id in self.idx:
            return Cterm(self.idx[term_id],self.type)
        else:
            return None
        
    def add_term(self,term_obj):
        """
        Adds a term object to the layer
        @type term_obj: L{Cterm}
        @param term_obj: the term object
        """
        self.node.append(term_obj.get_node())
           
    def add_external_reference(self,term_id, external_ref):
        """
        Adds an external reference for the given term
        @type term_id: string
        @param term_id: the term identifier
        @type external_ref: L{CexternalReference}
        @param external_ref: the external reference object
        """
        if term_id in self.idx:
            term_obj = Cterm(self.idx[term_id],self.type)
            term_obj.add_external_reference(external_ref)
        else:
            print term_id,' not in self.idx'

    def remove_terms(self,list_term_ids):
        """
        Removes a list of terms from the layer
        @type list_term_ids: list
        @param list_term_ids: list of term identifiers to be removed  
        """
        nodes_to_remove = set()
        for term in self:
            if term.get_id() in list_term_ids:
                nodes_to_remove.add(term.get_node())
                #For removing the previous comment
                prv = term.get_node().getprevious()
                if prv is not None:
                    nodes_to_remove.add(prv)
        
        for node in nodes_to_remove:
            self.node.remove(node)
        
