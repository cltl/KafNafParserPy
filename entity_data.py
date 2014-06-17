## Modified for KAF NAF adaptation
from lxml import etree
from lxml.objectify import dump
from references_data import *
    
    
class Centity:
    def __init__(self,node=None,type='NAF'):
        self.type = type
        if node is None:
            self.node = etree.Element('entity')
        else:
            self.node = node

    def get_node(self):
        return self.noce
                    
    def get_id(self):
        if self.type == 'NAF':
            return self.node.get('id')
        elif self.type == 'KAF':
            return self.node.get('eid')
    
    def get_type(self):
        return self.node.get('type')
    
    def get_references(self):
        for ref_node in self.node.findall('references'):
            yield Creferences(ref_node)
    
class Centities:
    def __init__(self,node=None,type='NAF'):
        self.type = type
        if node is None:
            self.node = etree.Element('entities')
        else:
            self.node = node
        

    def get_node(self):
        return self.node
                
    def to_kaf(self):
        if self.type == 'NAF':
            for node in self.__get_entity_nodes():
                node.set('eid',node.get('id'))
                del node.attrib['id']

    def to_naf(self):
        if self.type == 'KAF':
            for node in self.__get_entity_nodes():
                node.set('id',node.get('eid'))
                del node.attrib['eid']
                
    def __get_entity_nodes(self):
        for ent_node in self.node.findall('entity'):
            yield ent_node
                
    def __iter__(self):
        for ent_node in self.__get_entity_nodes():
            yield Centity(ent_node,self.type)
        
        
    def __str__(self):
        return dump(self.node)
