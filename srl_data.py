from span_data import *
from external_references_data import *
from lxml import etree

class Crole:
    def __init__(self,node):
        if node is None:
            self.node = etree.Element('role')
        else:
            self.node = node
            
    def get_node(self):
        return self.node
    
    def get_id(self):
        return self.node.get('id')
    
    def get_sem_role(self):
        return self.node.get('semRole')
    
    def get_external_references(self):
        node = self.node.find('externalReferences')
        if node is not None:
            ext_refs = CexternalReferences(node)
            for ext_ref in ext_refs:
                yield ext_ref
                
    def get_span(self):
        node = self.node.find('span')
        if node is not None:
            return Cspan(node)
        else:
            return None
    
class Cpredicate:
    def __init__(self,node):
        if node is None:
            self.node = etree.Element('predicate')
        else:
            self.node = node
            
    def get_node(self):
        return self.node
    
    def get_id(self):
        return self.node.get('id')
    
    def get_uri(self):
        return self.node.get('uri')
    
    def get_confidence(self):
        return self.node.get('confidence')
    
    def get_external_references(self):
        node = self.node.find('externalReferences')
        if node is not None:
            ext_refs = CexternalReferences(node)
            for ext_ref in ext_refs:
                yield ext_ref
                
    def get_roles(self):
        for node_role in self.node.findall('role'):
            yield Crole(node_role)

class Csrl:
    def __init__(self,node=None,type='NAF'):
        self.type = type
        if node is None:
            self.node = etree.Element('srl')
        else:
            self.node = node
            
    def get_node(self):
        return self.node
    
    def get_predicates(self):
        for node_pre in self.node.findall('predicate'):
            yield Cpredicate(node_pre)
            
            