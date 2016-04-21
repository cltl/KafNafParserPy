"""
This module is a parser for the sentiment elements in NAF/KAF terms
"""

# Modified for NAF KAF
from lxml import etree
from lxml.objectify import dump

class Cterm_sentiment:
    """
    This class encapsulates the sentiment element
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        self.type = 'NAF/KAF'
        if node is None:
            self.node = etree.Element('sentiment')
        else:
            self.node = node 
        #self.resource = self.polarity = self.strength = self.subjectivity = self.semantic_type = self.modifier = self.marker = self.product_feature = ''
        #if node is not None:
        #    self.resource = node.get('resource','')
        #    self.polarity = node.get('polarity','')
        #    self.strength = node.get('strength','')
        #    self.subjectivity = node.get('subjectivity','')
        #self.semantic_type = node.get('sentiment_semantic_type','')
        #    self.modifier = node.get('sentiment modifier','')
        #    self.marker = node.get('sentiment_marker','')
        #    self.product_feature = node.get('sentiment product feature','')
    
    def set_resource(self,r):
        """
        Sets the resource for the sentiment element
        @type r: string
        @param r: the resource for the element
        """
        self.node.set('resource',r)
    
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
    
    def get_polarity(self):
        """
        Returns the polarity of the element
        @rtype: string
        @return: the polarity of the element
        """
        return self.node.get('polarity')
    
    def set_polarity(self,p):
        """
        Sets the resource for the polarity element
        @type p: string
        @param p: the polarity for the element
        """
        self.node.set('polarity',p)
    
    def get_modifier(self):
        """
        Returns the modifier of the element
        @rtype: string
        @return: the modifier of the element
        """
        return self.node.get('sentiment_modifier')
    
    def set_modifier(self,sm):
        """
        Sets the sentiment modifier for the sentiment element
        @type sm: string
        @param sm: the modifier for the element
        """
        self.node.set('sentiment_modifier',sm)

    def __str__(self):
        return dump(self.node)
