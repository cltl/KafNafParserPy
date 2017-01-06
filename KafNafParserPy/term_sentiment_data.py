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

    def get_resource(self):
        """
        Returns the resource of the element
        @rtype: string
        @return: the resource of the element
        """
        return self.node.get('resource')

    def set_resource(self, r):
        """
        Sets the resource for the sentiment element
        @type r: string
        @param r: the resource for the element
        """
        self.node.set('resource', r)

    def get_strength(self):
        """
        Returns the strength of the element
        @rtype: string
        @return: the strength of the element
        """
        return self.node.get('strength')

    def set_strength(self, s):
        """
        Sets the strength for the sentiment element
        @type s: string
        @param s: the strength for the element
        """
        self.node.set('strength', s)

    def get_subjectivity(self):
        """
        Returns the subjectivity of the element
        @rtype: string
        @return: the subjectivity of the element
        """
        return self.node.get('subjectivity')

    def set_subjectivity(self, s):
        """
        Sets the subjectivity for the sentiment element
        @type s: string
        @param s: the subjectivity for the element
        """
        self.node.set('subjectivity', s)

    # old version of function (non standard name); leaving in case used somewhere
    def get_modifier(self):
        """
        Returns the sentiment modifier of the element
        @rtype: string
        @return: the sentiment modifier of the element
        """
        return self.node.get('sentiment_modifier')

    #old version of function (non standard name); leaving in case used somewhere
    def set_modifier(self,sm):
        """
        Sets the sentiment modifier for the sentiment element
        @type sm: string
        @param sm: the modifier for the element
        """
        self.node.set('sentiment_modifier',sm)

    def get_sentiment_modifier(self):
        """
        Returns the sentiment modifier of the element
        @rtype: string
        @return: the sentiment modifier of the element
        """
        return self.node.get('sentiment_modifier')

    def set_sentiment_modifier(self, sm):
        """
        Sets the sentiment modifier for the sentiment element
        @type sm: string
        @param sm: the sentiment modifier for the element
        """
        self.node.set('sentiment_modifier', sm)

    def get_sentiment_semantic_type(self):
        """
        Returns the sentiment semantic type of the element
        @rtype: string
        @return: the sentiment semantic type of the element
        """
        return self.node.get('sentiment_semantic_type')

    def set_sentiment_semantic_type(self, st):
        """
        Sets the sentiment semantic type for the sentiment element
        @type st: string
        @param st: the sentiment semantic type for the element
        """
        self.node.set('sentiment_semantic_type', st)

    def get_sentiment_marker(self):
        """
        Returns the sentiment marker of the element
        @rtype: string
        @return: the sentiment marker of the element
        """
        return self.node.get('sentiment_marker')

    def set_sentiment_marker(self, sm):
        """
        Sets the sentiment marker for the sentiment element
        @type sm: string
        @param sm: the sentiment marker for the element
        """
        self.node.set('sentiment_marker', sm)

    def get_sentiment_product_feature(self):
        """
        Returns the sentiment product feature of the element
        @rtype: string
        @return: the sentiment product feature of the element
        """
        return self.node.get('sentiment_product_feature')

    def set_sentiment_product_feature(self, spf):
        """
        Sets the sentiment product feature for the sentiment element
        @type sm: string
        @param sm: the sentiment product feature for the element
        """
        self.node.set('sentiment_product_feature', spf)

    def __str__(self):
        return dump(self.node)
