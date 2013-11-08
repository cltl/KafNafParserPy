from lxml import etree
from lxml.objectify import dump
from references_data import *
    
    
class entity:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('entity')
        else:
            self.node = node
            
    def get_id(self):
        return self.node.get('id')
    
    def get_type(self):
        return self.node.get('type')
    
    def get_references(self):
        for ref_node in self.node.findall('references'):
            yield references(ref_node)
    
class entities:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('entities')
        else:
            self.node = node
        
    def __get_entity_nodes(self):
        for ent_node in self.node.findall('entity'):
            yield ent_node
                
    def __iter__(self):
        for ent_node in self.__get_entity_nodes():
            yield entity(ent_node)
        
        
    def __str__(self):
        return dump(self.node)
