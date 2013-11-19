from lxml import etree
from lxml.objectify import dump


class Cdependency:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('dep')
        else:
            self.node = node
            
            
    def get_from(self):
        return self.node.get('from')
    
    def get_to(self):
        return self.node.get('to')
    
    def get_function(self):
        return self.node.get('rfunc')
    
    
    def __str__(self):
        return dump(self.node)



class Cdependencies:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('deps')
        else:
            self.node = node
            
    def __str__(self):
        return dump(self.node)


    def __get_node_deps(self):
        for node_dep in self.node.findall('dep'):
            yield node_dep
            
    def get_dependencies(self):
        for node in self.__get_node_deps():
            yield Cdependency(node)
            