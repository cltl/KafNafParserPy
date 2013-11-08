from lxml import etree
from lxml.objectify import dump
from references_data import *



class Cproperty:
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
            yield Creferences(ref_node)
                             
                        
                
class Cproperties:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('properties')
        else:
            self.node = node
            
    def __iter__(self):
        for prop_node in self.node.findall('property'):
            yield Cproperty(prop_node)
                
class Cfeatures:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('features')
        else:
            self.node = node
            
    def get_properties(self):
        node_prop = self.node.find('properties')
        if node_prop is not None:
            obj_properties = Cproperties(node_prop)
            for prop in obj_properties:
                yield prop
                