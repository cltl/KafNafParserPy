from lxml import etree
from lxml.objectify import dump


class Cholder:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('opinion_holder')
        else:
            self.node = node    
    
    def set_span(self,my_span):
        self.node.append(my_span.get_node())
        
    def __str__(self):
        return dump(self.node)  
    
    def get_node(self):
        return self.node
        

class Ctarget:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('opinion_target')
        else:
            self.node = node    
    
    def set_span(self,my_span):
        self.node.append(my_span.get_node())  
        
    def __str__(self):
        return dump(self.node)  

    def get_node(self):
        return self.node
        
        
class Cexpression:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('opinion_expression')
        else:
            self.node = node    
    
    def set_polarity(self,pol):
        self.node.set('polarity',pol)
        
    def set_strength(self,st):
        self.node.set('strength',st)
        
    def set_span(self,my_span):
        self.node.append(my_span.get_node())

    def __str__(self):
        return dump(self.node)  
    
    def get_node(self):
        return self.node

class Copinion:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('opinion')
        else:
            self.node = node  
    
    def set_id(self,my_id):
        self.node.set('id',my_id)
        
    def set_holder(self,hol):
        self.node.append(hol.get_node())

    def set_target(self,tar):
        self.node.append(tar.get_node())
        
    def set_expression(self,exp):
        self.node.append(exp.get_node())
        
    def __str__(self):
        return dump(self.node)  
    
    def get_node(self):
        return self.node
    
    



class Copinions:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('opinions')
        else:
            self.node = node
    def add_opinion(self,opi_obj):
        self.node.append(opi_obj.get_node())
                         
    def get_node(self):
        return self.node