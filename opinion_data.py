#Modified for KAF NAF ok

from lxml import etree
from lxml.objectify import dump
from span_data import *



class Cholder:
    def __init__(self,node=None):
        self.type = 'NAF/KAF'
        if node is None:
            self.node = etree.Element('opinion_holder')
        else:
            self.node = node    
    
    def set_span(self,my_span):
        self.node.append(my_span.get_node())

    def set_comment(self,c):
        c = c.replace('--','- -')
        self.node.insert(0,etree.Comment(c) )
        
    def get_span(self):
        span_obj = self.node.find('span')
        if span_obj is not None:
            return Cspan(span_obj)
        return None
        
    def __str__(self):
        return dump(self.node)  
    
    def get_node(self):
        return self.node
        

class Ctarget:
    def __init__(self,node=None):
        self.type = 'NAF/KAF'
        if node is None:
            self.node = etree.Element('opinion_target')
        else:
            self.node = node    
    
    def set_comment(self,c):
        c = c.replace('--','- -')
        self.node.insert(0,etree.Comment(c) )
        
    def get_comment(self):
        return self.node_comment
        
    def set_span(self,my_span):
        self.node.append(my_span.get_node())  
    
    def get_span(self):
        span_obj = self.node.find('span')
        if span_obj is not None:
            return Cspan(span_obj)
        return None
    
    def __str__(self):
        return dump(self.node)  

    def get_node(self):
        return self.node
        
        
class Cexpression:
    def __init__(self,node=None):
        self.type = 'NAF/KAF'
        if node is None:
            self.node = etree.Element('opinion_expression')
        else:
            self.node = node   

    def set_comment(self,c):
        c = c.replace('--','- -')
        self.node.insert(0,etree.Comment(c)) 
    
    def set_polarity(self,pol):
        self.node.set('polarity',pol)
        
    def get_polarity(self):
        return self.node.get('polarity')
        
    def set_strength(self,st):
        self.node.set('strength',st)
        
    def get_strength(self):
        return self.node.get('strength')
        
    def set_span(self,my_span):
        self.node.append(my_span.get_node())
        
    def get_span(self):
        span_obj = self.node.find('span')
        if span_obj is not None:
            return Cspan(span_obj)
        return None

    def __str__(self):
        return dump(self.node)  
    
    def get_node(self):
        return self.node

class Copinion:
    def __init__(self,node=None,type='NAF'):
        self.type = type
        if node is None:
            self.node = etree.Element('opinion')
        else:
            self.node = node  
            
    def set_comment(self,c):
        c = c.replace('--','- -')
        self.node.insert(0,etree.Comment(c) )
    
    def set_id(self,my_id):
        if self.type == 'NAF':
            self.node.set('id',my_id)
        elif self.type == 'KAF':
            self.node.set('oid',my_id)
            
    def get_id(self):
        if self.type == 'NAF':
            return self.node.get('id')
        elif self.type == 'KAF':
            return self.node.get('oid')        
        
    def set_holder(self,hol):
        self.node.append(hol.get_node())
        
    def get_holder(self):
        node_hol = self.node.find('opinion_holder')
        if node_hol is not None:
            return Cholder(node_hol)
        else:
            return None

    def set_target(self,tar):
        self.node.append(tar.get_node())
        
    def get_target(self):
        node_target = self.node.find('opinion_target')
        if node_target is not None:
            return Ctarget(node_target)
        else:
            return None
        
    def set_expression(self,exp):
        self.node.append(exp.get_node())

    def get_expression(self):
        node_exp = self.node.find('opinion_expression')
        if node_exp is not None:
            return Cexpression(node_exp)
        else:
            return None
        
    def __str__(self):
        return dump(self.node)  
    
    def get_node(self):
        return self.node
    
    



class Copinions:
    def __init__(self,node=None,type='NAF'):
        self.type = type
        if node is None:
            self.node = etree.Element('opinions')
        else:
            self.node = node
            
    def __get_opinion_nodes(self):
        for node in self.node.findall('opinion'):
            yield node
            
    def get_opinions(self):
        for node in self.__get_opinion_nodes():
            yield Copinion(node,self.type)
            
    def to_kaf(self):
        if self.type == 'NAF':
            for node in self.__get_opinion_nodes():
                node.set('oid',node.get('id'))
                del node.attrib['id']

    def to_naf(self):
        if self.type == 'KAF':
            for node in self.__get_opinion_nodes():
                node.set('id',node.get('oid'))
                del node.attrib['oid']                
            
            
    def add_opinion(self,opi_obj):
        self.node.append(opi_obj.get_node())
                         
    def get_node(self):
        return self.node