"""
This module parses the constituency tree layer in KAF/NAF
"""

from lxml import etree
from lxml.objectify import dump
from span_data import Cspan


class Cnonterminal:
    """
    This class encapsulates a non terminal object
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        if node is None:
            self.node = etree.Element('nt')
        else:
            self.node = node
            
    def get_id(self):
        """
        Returns the identifier of the object
        @rtype: string
        @return: the non terminal identifier
        """
        return self.node.get('id')
    
    def get_label(self):
        """
        Returns the label of the object
        @rtype: string
        @return: the label of the object
        """
        return self.node.get('label')

    def __str__(self):
        return dump(self.node)
            


class Cterminal:
    """
    This class encapsulates a terminal object
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        if node is None:
            self.node = etree.Element('t')
        else:
            self.node = node
            
    def get_id(self):
        """
        Returns the identifier of the object
        @rtype: string
        @return: identifier of the terminal object
        """
        return self.node.get('id')
    
    def get_span(self):
        """
        Returns the term span of the object
        @rtype: L{Cspan}
        @return: the span object
        """
        span_node = self.node.find('span')
        return Cspan(span_node)
    
    def __str__(self):
        return dump(self.node)
            
class Cedge:
    """
    This class encapsulates an edge object
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        if node is None:
            self.node = etree.Element('edge')
        else:
            self.node = node
            
    def __str__(self):
        return dump(self.node)
    
    def get_from(self):
        """
        Returns the from label
        @rtype: string
        @return: the from label of the relation
        """
        return self.node.get('from')
    
    def get_to(self):
        """
        Returns the to label
        @rtype: string
        @return:  the to label of the relation
        """
        return self.node.get('to')
            


class Ctree:
    """
    This class encapsulates a tree object
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
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
        """
        Iterator that returns all the non terminal objects
        @rtype: L{Cnonterminal}
        @return: non terminal objects (iterator)
        """
        for nt_node in self.__get_nt_nodes():
            yield Cnonterminal(nt_node)
    ##################################
            
    ## Fore getting  terminals
    def __get_t_nodes(self):
        for t_node in self.node.findall('t'):
            yield t_node

    def get_terminals(self):
        """
        Iterator that returns all the terminal objects
        @rtype: L{Cterminal}
        @return: terminal objects (iterator)
        """
        for t_node in self.__get_t_nodes():
            yield Cterminal(t_node)
    ##################################            
            
     ## Fore getting  edges
    def __get_edge_nodes(self):
        for t_node in self.node.findall('edge'):
            yield t_node

    def get_edges(self):
        """
        Iterator that returns all the edge objects
        @rtype: L{Cedge}
        @return: terminal objects (iterator)
        """
        for edge_node in self.__get_edge_nodes():
            yield Cedge(edge_node)
    ##################################          
            
    

class Cconstituency:
    """
    This class encapsulates the constituency layer
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        self.type = 'NAF/NAF'
        if node is None:
            self.node = etree.Element('constituency')
        else:
            self.node = node

    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
                    
    def to_kaf(self):
        pass
    
    def to_naf(self):
        pass
    
    def __get_tree_nodes(self):
        for tree_node in self.node.findall('tree'):
            yield tree_node
    
    def get_trees(self):
        """
        Iterator that returns all the tree objects
        @rtype: L{Ctree}
        @return: tree objects (iterator)
        """
        for tree_node in self.__get_tree_nodes():
            yield Ctree(tree_node)
            
    def __str__(self):
        return dump(self.node)