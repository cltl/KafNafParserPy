"""
Parser for the references objects in KAF/NAF
"""
# Modified for NAF/KAf
from lxml import etree

from .span_data import Cspan


class Creferences:
    """
    This class encapsulates the references objects in KAF/NAF
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        self.type = 'NAF/KAF'
        if node is None:
            self.node = etree.Element('references')
        else:
            self.node = node
            
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
    
    def __iter__(self):
        """
        Iterator that returns all the span objects in the reference
        @rtype: L{Cspan}
        @return: list of span objects (iterator)
        """
        for span_node in self.node.findall('span'):
            yield Cspan(span_node)
            
    def add_span(self,term_span):
        """
        Adds a list of term ids a new span in the references
        @type term_span: list
        @param term_span: list of term ids
        """
        new_span = Cspan()
        new_span.create_from_ids(term_span)
        self.node.append(new_span.get_node())

    def get_span(self):
        """
        Returns the span object of the reference
        @rtype: L{Cspan}
        @return: the term span
        """
        node_span = self.node.find('span')
        if node_span is not None:
            return Cspan(node_span)
        else:
            return None
    
    def set_span(self,this_span):
        """
        Sets the span for the lemma
        @type this_span: L{Cspan}
        @param this_span: lemma identifier
        """
        self.node.append(this_span.get_node())
        
        
