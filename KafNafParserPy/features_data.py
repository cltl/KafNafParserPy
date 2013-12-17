from lxml import etree
from lxml.objectify import dump
from references_data import *



class Cproperty:
    def __init__(self,node=None,type='NAF'):
        self.type = type
        if node is None:
            self.node = etree.Element('property')
        else:
            self.node = node
    
    def get_id(self):
        if self.type == 'KAF':
            return self.node.get('pid')
        elif self.type == 'NAF':
            return self.node.get('id')
    
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
    def __init__(self,node=None,type='NAF'):
        self.type = type
        if node is None:
            self.node = etree.Element('features')
        else:
            self.node = node
        
    def to_kaf(self):
        if self.type == 'NAF':
            ##convert all the properties
            for node in self.node.findall('properties/property'):
                node.set('pid',node.get('id'))
                del node.attrib['id']

    def to_naf(self):
        if self.type == 'KAF':
            ##convert all the properties
            for node in self.node.findall('properties/property'):
                node.set('id',node.get('pid'))
                del node.attrib['pid']                
            
        
    def get_properties(self):
        node_prop = self.node.find('properties')
        if node_prop is not None:
            obj_properties = Cproperties(node_prop,self.type)
            for prop in obj_properties:
                yield prop
                