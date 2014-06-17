from lxml import etree
from lxml.objectify import dump
from span_data import Cspan


class Cnonterminal:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('nt')
        else:
            self.node = node
            
    def get_id(self):
        return self.node.get('id')
    
    def get_label(self):
        return self.node.get('label')

    def __str__(self):
        return dump(self.node)
            


class Cterminal:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('t')
        else:
            self.node = node
            
    def get_id(self):
        return self.node.get('id')
    
    def get_span(self):
        span_node = self.node.find('span')
        return Cspan(span_node)
    
    def __str__(self):
        return dump(self.node)
            
class Cedge:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('edge')
        else:
            self.node = node
            
    def __str__(self):
        return dump(self.node)
    
    def get_from(self):
        return self.node.get('from')
    
    def get_to(self):
        return self.node.get('to')
            


class Ctree:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('tree')
        else:
            self.node = node
            

    def __str__(self):
        return dump(self.node)
    
    ## Fore getting non terminals
    def __get_nt_nodes(self):
        for nt_node in self.node.findall('nt'):
            yield nt_node

    def get_non_terminals(self):
        for nt_node in self.__get_nt_nodes():
            yield Cnonterminal(nt_node)
    ##################################
            
    ## Fore getting  terminals
    def __get_t_nodes(self):
        for t_node in self.node.findall('t'):
            yield t_node

    def get_terminals(self):
        for t_node in self.__get_t_nodes():
            yield Cterminal(t_node)
    ##################################            
            
     ## Fore getting  edges
    def __get_edge_nodes(self):
        for t_node in self.node.findall('edge'):
            yield t_node

    def get_edges(self):
        for edge_node in self.__get_edge_nodes():
            yield Cedge(edge_node)
    ##################################          
            
    

class Cconstituency:
    def __init__(self,node=None):
        self.type = 'NAF/NAF'
        if node is None:
            self.node = etree.Element('constituency')
        else:
            self.node = node

    def get_node(self):
        return self.node
                    
    def to_kaf(self):
        pass
    
    def to_naf(self):
        pass
    
    def __get_tree_nodes(self):
        for tree_node in self.node.findall('tree'):
            yield tree_node
    
    def get_trees(self):
        for tree_node in self.__get_tree_nodes():
            yield Ctree(tree_node)
            
    def __str__(self):
        return dump(self.node)