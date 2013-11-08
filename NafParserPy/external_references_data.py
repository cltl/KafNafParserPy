from term_sentiment_data import Cterm_sentiment
from lxml import etree

class CexternalReference:
    def __init__(self,node=None):
        #self.resource = self.reference = self.reftype = self.status = self.source = self.confidence = ''
        if node is None:
            self.node = etree.Element('externalRef')
        else:
            self.node = node
        
    def get_node(self):
        return self.node
        
    def set_resource(self,resource):
        self.node.set('resource',resource)
    
    def set_confidence(self,confidence):
        self.node.set('confidence',confidence)
    
    def set_reference(self,reference):
        self.node.set('reference',reference)
        

class CexternalReferences:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('externalReferences')
        else:
            self.node = node
                
    def add_external_reference(self,ext_ref):
        self.node.append(ext_ref.get_node())
        
    def get_node(self):
        return self.node
        
 
    