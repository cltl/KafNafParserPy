# included code for NAF/KAF


from span_data import *
from external_references_data import *
from term_sentiment_data import *
from lxml import etree


class Cterm:
    def __init__(self,node=None,type='NAF'):
        self.type = type
        if node is None:
            self.node = etree.Element('term')
        else:
            self.node = node

    def get_node(self):
        return self.node
            
    def get_id(self):
        if self.type == 'NAF':
            return self.node.get('id')
        elif self.type == 'KAF':
            return self.node.get('tid')
    
    def get_lemma(self):
        return self.node.get('lemma')
    
    def get_pos(self):
        return self.node.get('pos')
    
    def get_morphofeat(self):
        return self.node.get('morphofeat')
    
    def get_span(self):
        node_span = self.node.find('span')
        if node_span is not None:
            return Cspan(node_span)
        else:
            return None
        
    def get_sentiment(self):
        sent_node = self.node.find('sentiment')
        
        if sent_node is None:
            return None
        else:
            return Cterm_sentiment(sent_node)
        
        
    def add_external_reference(self,ext_ref):
        ext_refs_node = self.node.find('externalReferences')
        if ext_refs_node is None:
            ext_refs_obj = CexternalReferences()
            self.node.append(ext_refs_obj.get_node())
        else:
            ext_refs_obj = CexternalReferences(ext_refs_node)
            
        ext_refs_obj.add_external_reference(ext_ref)
        
    def add_term_sentiment(self,term_sentiment):
        self.node.append(term_sentiment.get_node())
            
           
        
    
class Cterms:
    def __init__(self,node=None,type='NAF'):
        self.idx = {}
        self.type = type
        if node is None:
            self.node = etree.Element('terms')
        else:
            self.node = node
            for node_term in self.__get_node_terms():
                self.idx[node_term.get('id')] = node_term    
    
    def get_node(self):
        return self.node
    
    def to_kaf(self):
        if self.type == 'NAF':
            self.type = 'KAF'
            for node in self.__get_node_terms():
                node.set('tid',node.get('id'))
                del node.attrib['id']

    def to_naf(self):
        if self.type == 'KAF':
            self.type = 'NAF'
            for node in self.__get_node_terms():
                node.set('id',node.get('tid'))
                del node.attrib['tid']
                
    def __get_node_terms(self):
        for node_term in self.node.findall('term'):
            yield node_term
            
    def __iter__(self):
        for node_term in self.__get_node_terms():
            yield Cterm(node_term,self.type)
            
    def get_term(self,term_id):
        if term_id in self.idx:
            return Cterm(self.idx[term_id],self.type)
        else:
            return None
           
    def add_external_reference(self,term_id, external_ref):
        if term_id in self.idx:
            term_obj = Cterm(self.idx[term_id],self.type)
            term_obj.add_external_reference(external_ref)

    def remove_terms(self,list_term_ids):
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
        