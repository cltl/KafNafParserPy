from lxml import etree
from lxml.objectify import dump

class term_sentiment:
    def __init__(self,node=None):
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
    
    def get_polarity(self):
        return self.node.get('polarity')
    
    def get_modifier(self):
        return self.node.get('sentiment_modifier')

    def __str__(self):
        return dump(self.node)
