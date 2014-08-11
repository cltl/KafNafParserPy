"""
Parser for the external references object in KAF/NAF
"""

# included modification for KAF/NAF
from term_sentiment_data import Cterm_sentiment
from lxml import etree

class CexternalReference:
    """
    This class encapsulates the external reference object in KAF/NAF
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        self.type= 'NAF/KAF'
        #self.resource = self.reference = self.reftype = self.status = self.source = self.confidence = ''
        if node is None:
            self.node = etree.Element('externalRef')
        else:
            self.node = node
        
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
        
    def get_external_references(self):
        """
        Returns the external references of an external reference (can be nested)
        @rtype: L{CexternalReference}
        @return: iterator of external references
        """
        for node in self.node.findall('externalRef'):
            yield CexternalReference(node)
            
    def add_external_reference(self,ext_ref):
        self.node.append(ext_ref.get_node())
                
    def set_resource(self,resource):
        """
        Sets the resource for the element
        @type resource: string
        @param resource: the resource of the element
        """
        self.node.set('resource',resource)
    
    def set_confidence(self,confidence):
        """
        Sets the confidence for the element
        @type confidence: string
        @param confidence: the confidence of the element
        """
        self.node.set('confidence',confidence)
    
    def set_reference(self,reference):
        """
        Sets the reference for the element
        @type reference: string
        @param reference: the reference of the element
        """
        self.node.set('reference',reference)

    def get_resource(self):
        """
        Returns the resource of the element
        @rtype: string
        @return: the resource of the element
        """
        return self.node.get('resource')
        
    def get_confidence(self):
        """
        Returns the confidence of the element
        @rtype: string
        @return: the confidence of the element
        """
        return self.node.get('confidence')
        
    def get_reference(self):
        """
        Returns the reference attribute of the element
        @rtype: string
        @return: the reference attribute of the element
        """
        return self.node.get('reference')       
    
    def set_reftype(self,r):
        """
        Sets the reftype for the element
        @type r: string
        @param r: the reftype of the element
        """
        self.node.set('reftype',r) 
        
    def get_reftype(self):
        """
        Returns the reftype attribute of the element
        @rtype: string
        @return: the reftype attribute of the element
        """
        return self.node.get('reftype')

class CexternalReferences:
    """
    This class encapsulates the external references object, which is a set of external reference objects
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        if node is None:
            self.node = etree.Element('externalReferences')
        else:
            self.node = node
                
    def add_external_reference(self,ext_ref):
        """
        Adds an external reference to the layer
        @type ext_ref: L{CexternalReference}
        @param ext_ref: an external reference object  
        """
        self.node.append(ext_ref.get_node())
        
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
        
    def __iter__(self):
        """
        Iterator that returns all the external reference objects
        @rtype: L{CexternalReference}
        @return: list of external references (iterator)
        """
        for node in self.node.findall('externalRef'):
            yield CexternalReference(node)
 
    