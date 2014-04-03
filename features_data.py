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
    
    def get_node(self):
        return self.node
    
    def get_id(self):
        if self.type == 'KAF':
            return self.node.get('pid')
        elif self.type == 'NAF':
            return self.node.get('id')
  
    def set_id(self,pid):
        if self.type == 'KAF':
            return self.node.set('pid',pid)
        elif self.type == 'NAF':
            return self.node.set('id',pid)
          
    def get_type(self):
        return self.node.get('lemma')

    def set_type(self,t):
        return self.node.set('lemma',t)
    
    def get_references(self):
        for ref_node in self.node.findall('references'):
            yield Creferences(ref_node)
            
    def set_reference(self,ref):
        self.node.append(ref.get_node())
                             
                        
                
class Cproperties:
    def __init__(self,node=None,type='NAF'):
        self.type=type
        if node is None:
            self.node = etree.Element('properties')
        else:
            self.node = node
            
    def get_node(self):
        return self.node
            
    def __iter__(self):
        for prop_node in self.node.findall('property'):
            yield Cproperty(prop_node,self.type)
            
    def add_property(self,pid, label,term_span):
        new_property = Cproperty(type=self.type)
        self.node.append(new_property.get_node())
        ##Set the id
        if pid is None:
            ##Generate a new pid
            existing_pids = [property.get_id() for property in self]
            n = 0
            new_pid = ''
            while True:
                new_pid = 'p'+str(n)
                if new_pid not in existing_pids: break
                n += 1
            pid = new_pid
        new_property.set_id(pid)
        
        new_property.set_type(label)
        
        new_ref = Creferences()
        new_ref.add_span(term_span)
        new_property.set_reference(new_ref)
 
        
                
class Cfeatures:
    def __init__(self,node=None,type='NAF'):
        self.type = type
        if node is None:
            self.node = etree.Element('features')
        else:
            self.node = node
        
    def get_node(self):
        return self.node
    
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
            
    def add_property(self,pid, label,term_span):
        node_prop = self.node.find('properties')
        if node_prop is None:
            properties = Cproperties(type=self.type)
            self.node.append(properties.get_node())
        else:
            properties = Cproperties(node=node_prop,type=self.type)
            
        properties.add_property(pid, label,term_span)
        
        
    def get_properties(self):
        node_prop = self.node.find('properties')
        if node_prop is not None:
            obj_properties = Cproperties(node_prop,self.type)
            for prop in obj_properties:
                yield prop
                
    def remove_properties(self):
        node_prop = self.node.find('properties')
        if node_prop is not None:
            self.node.remove(node_prop)
            