from lxml import etree
from lxml.objectify import dump
from references_data import *



class property:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('property')
        else:
            self.node = node
    
    def get_id(self):
        return self.node.get('pid')
    
    def get_type(self):
        return self.node.get('lemma')
    
    def get_references(self):
        for ref_node in self.node.findall('references'):
            yield references(ref_node)
                             
                        
                
class properties:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('properties')
        else:
            self.node = node
            
    def __iter__(self):
        for prop_node in self.node.findall('property'):
            yield property(prop_node)
                
class features:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('features')
        else:
            self.node = node
            
    def get_properties(self):
        node_prop = self.node.find('properties')
        if node_prop is not None:
            obj_properties = properties(node_prop)
            for prop in obj_properties:
                yield prop
                