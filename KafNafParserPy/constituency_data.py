"""
This module parses the constituency tree layer in KAF/NAF
"""

from lxml import etree
from lxml.objectify import dump

from .span_data import Cspan


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
            
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
            
    def get_id(self):
        """
        Returns the identifier of the object
        @rtype: string
        @return: the non terminal identifier
        """
        return self.node.get('id')
    
    def set_id(self,this_id):
        """
        Sets the identifier for the element
        @param this_id: identifier
        @type this_id: string
        """
        self.node.set('id',this_id)
    
    def get_label(self):
        """
        Returns the label of the object
        @rtype: string
        @return: the label of the object
        """
        return self.node.get('label')
    
    def set_label(self,label):
        """
        Sets the label of the non terminal
        @param label: label
        @type label: string
        """
        self.node.set('label',label)
        

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
            
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
            
    def get_id(self):
        """
        Returns the identifier of the object
        @rtype: string
        @return: identifier of the terminal object
        """
        return self.node.get('id')
    
    def set_id(self,this_id):
        """
        Sets the identifier for the element
        @param this_id: identifier
        @type this_id: string
        """
        self.node.set('id',this_id)
    
    def get_span(self):
        """
        Returns the term span of the object
        @rtype: L{Cspan}
        @return: the span object
        """
        span_node = self.node.find('span')
        return Cspan(span_node)
    
    def set_span(self,this_span):
        """
        Sets the span for the terminal
        @type this_span: L{Cspan}
        @param this_span: span
        """
        self.node.append(this_span.get_node())
    
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
            
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
    
    def get_id(self):
        """
        Returns the identifier of the object
        @rtype: string
        @return: identifier of the terminal object
        """
        return self.node.get('id')
    
    def set_id(self,this_id):
        """
        Sets the identifier for the element
        @param this_id: identifier
        @type this_id: string
        """
        self.node.set('id',this_id)
        
    def __str__(self):
        return dump(self.node)
    
    def get_from(self):
        """
        Returns the from label
        @rtype: string
        @return: the from label of the relation
        """
        return self.node.get('from')
    
    def set_from(self,this_from):
        """
        Sets the identifier for the element
        @param this_from: from label
        @type this_from: string
        """
        self.node.set('from',this_from)
    
    def get_to(self):
        """
        Returns the to label
        @rtype: string
        @return:  the to label of the relation
        """
        return self.node.get('to')
    
    def set_to(self,this_to):
        """
        Sets the identifier for the element
        @param this_to: to label
        @type this_to: string
        """
        self.node.set('to',this_to)
        
    def set_as_head(self):
        """
        Sets the edge as a head element
        """
        self.node.set('head','yes')
        
    def set_comment(self,c):
        """
        Sets the comment for the element
        @type c: string
        @param c: comment for the element
        """
        c = c.replace('--','- -')
        self.node.insert(0,etree.Comment(c) )

    def get_head(self):
        """
        Returns whether the from is head of the constituent (None if not)
        @rtype: string
        @return:  the to label of the relation
        """
        
        return self.node.get('head')
            


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
            
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node

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
            

    def get_terminals_as_list(self):
        """
        Iterator that returns all the terminal objects
        @rtype: L{Cterminal}
        @return: terminal objects as list
        """
        terminalList = []
        for t_node in self.__get_t_nodes():
            terminalList.append(Cterminal(t_node))
        return terminalList

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
    
    def append_element(self,this_element):
        """
        Appends a node to the tree, could be a terminal or non terminal or edge
        @param this_element: the element to be appended
        @type this_element: object
        """
        self.node.append(this_element.get_node())        

    def get_edges_as_list(self):
        """
        Iterator that returns all the edge objects
        @rtype: L{Cedge}
        @return: terminal objects (iterator)
        """
        my_edges = []
        for edge_node in self.__get_edge_nodes():
            my_edges.append(Cedge(edge_node))
        return my_edges
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
    
    def add_tree(self,this_tree):
        """
        Adds a tree to the constituency layer
        @param this_tree: the constituency tree
        @type this_tree: L{Ctree}
        """
        self.node.append(this_tree.get_node())
