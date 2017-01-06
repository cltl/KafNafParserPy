"""
This is a parser for opinions in KAF/NAF files
"""

from lxml import etree
from lxml.objectify import dump

from .span_data import *



class Cholder:
    """
    This class encapsulates the holder of the opinions
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        self.type = 'NAF/KAF'
        if node is None:
            self.node = etree.Element('opinion_holder')
        else:
            self.node = node    
    
    def set_span(self,my_span):
        """
        Sets the span with the provided span object
        @type my_span: L{Cspan}
        @param my_span: span object
        """
        self.node.append(my_span.get_node())

        
    def get_span(self):
        """
        Returns the span of the object
        @rtype: L{Cspan}
        @return: the span object
        """
        span_obj = self.node.find('span')
        if span_obj is not None:
            return Cspan(span_obj)
        return None
    
    def set_comment(self,c):
        """
        Sets the comment for the element
        @type c: string
        @param c: comment for the element
        """
        c = ' '+c.replace('-','').strip()+' '
        self.node.insert(0,etree.Comment(c))


    def get_comment(self):
        """
        Returns the comment
        @rtype: string
        @return: the comment
        """
        return self.node_comment


    def set_type(self,t):
        """
        Sets the type of holder
        @type t: string
        @param t: type of holder
        """
        self.node.set('type',t)
    
    def get_type(self):
        """
        Returns the type of holder
        @rtype: string
        @return: the type of holder
        """
        return self.node.get('type')
        
    def __str__(self):
        return dump(self.node)  
    
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
        

class Ctarget:
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        self.type = 'NAF/KAF'
        if node is None:
            self.node = etree.Element('opinion_target')
        else:
            self.node = node    
    
    def set_comment(self,c):
        """
        Sets the comment for the element
        @type c: string
        @param c: comment for the element
        """
        c = ' '+c.replace('-','').strip()+' ' 
        self.node.insert(0,etree.Comment(c) )
        
    def get_comment(self):
        """
        Returns the comment
        @rtype: string
        @return: the comment
        """
        return self.node_comment
        
    def set_span(self,my_span):
        """
        Sets the span with the provided span object
        @type my_span: L{Cspan}
        @param my_span: span object
        """
        self.node.append(my_span.get_node())  
    
    def get_span(self):
        """
        Returns the span of the object
        @rtype: L{Cspan}
        @return: the span object
        """
        span_obj = self.node.find('span')
        if span_obj is not None:
            return Cspan(span_obj)
        return None
    
    def __str__(self):
        return dump(self.node)  

    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
        
        
class Cexpression:

    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        self.type = 'NAF/KAF'
        if node is None:
            self.node = etree.Element('opinion_expression')
        else:
            self.node = node   

    def set_comment(self,c):
        """
        Sets the comment for the element
        @type c: string
        @param c: comment for the element
        """
        c = ' '+c.replace('-','').strip()+' ' 
        self.node.insert(0,etree.Comment(c))
    
    
    def get_comment(self):
        """
        Returns the comment
        @rtype: string
        @return: the comment
        """
        return self.node_comment
    
    def set_polarity(self,pol):
        """
        Sets the polarity for the expression
        @type pol: string
        @param pol: polarity for the expression
        """
        self.node.set('polarity',pol)
        
    def get_polarity(self):
        """
        Returns the polarity for the expression
        @rtype: string
        @return: the polarity for the expression
        """
        return self.node.get('polarity')
        
    def set_strength(self,st):
        """
        Sets the strength for the expression
        @type st: string
        @param st: strength for the expression
        """
        self.node.set('strength',st)
        
    def get_strength(self):
        """
        Returns the strength for the expression
        @rtype: string
        @return: the strength for the expression
        """
        return self.node.get('strength')
    
    def set_subjectivity(self,s):
        """
        Sets the subjectivity for the expression
        @type s: string
        @param s: subjectivity for the expression
        """
        self.node.set('subjectivity',s)
    
    def get_subjectivity(self):
        """
        Returns the subjectivity for the expression
        @rtype: string
        @return: the subjectivity for the expression
        """
        return self.node.get('subjectivity')
    
    
    def set_sentiment_semantic_type(self,sst):
        """
        Sets the sentiment_semantic_type for the expression
        @type sst: string
        @param sst: sentiment_semantic_type for the expression
        """
        self.node.set('sentiment_semantic_type',sst)
    
    def get_sentiment_semantic_type(self):
        """
        Returns the sentiment_semantic_type for the expression
        @rtype: string
        @return: the sentiment_semantic_type for the expression
        """
        return self.node.get('sentiment_semantic_type')
    
    
    def set_sentiment_product_feature(self,spf):
        """
        Sets the sentiment_product_feature for the expression
        @type spf: string
        @param spf: sentiment_product_feature for the expression
        """
        self.node.set('sentiment_product_feature',spf)
    
    def get_sentiment_product_feature(self):
        """
        Returns the sentiment_product_feature for the expression
        @rtype: string
        @return: the sentiment_product_feature for the expression
        """
        return self.node.get('sentiment_product_feature')
    
    def set_span(self,my_span):
        """
        Sets the span with the provided span object
        @type my_span: L{Cspan}
        @param my_span: span object
        """
        self.node.append(my_span.get_node())
        
    def get_span(self):
        """
        Returns the span of the object
        @rtype: L{Cspan}
        @return: the span object
        """
        span_obj = self.node.find('span')
        if span_obj is not None:
            return Cspan(span_obj)
        return None

    def __str__(self):
        return dump(self.node)  
    
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node

class Copinion:
    """
    This class encapsulates KAF/NAF opinion elements
    """
    def __init__(self,node=None,type='NAF'):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        @type type: string
        @param type: the type of the object (KAF or NAF)
        """
        self.type = type
        if node is None:
            self.node = etree.Element('opinion')
        else:
            self.node = node  
            
    def set_comment(self,c):
        """
        Sets the comment for the element
        @type c: string
        @param c: comment for the element
        """
        c = ' '+c.replace('-','').strip()+' '
        self.node.insert(0,etree.Comment(c) )
    
    def set_id(self,my_id):
        """
        Sets the opinion identifier
        @type my_id: string
        @param my_id: the opinion identifier
        """
        if self.type == 'NAF':
            self.node.set('id',my_id)
        elif self.type == 'KAF':
            self.node.set('oid',my_id)
            
    def get_id(self):
        """
        Returns the opinion identifier
        @rtype: string
        @return: the opinion identifier
        """
        if self.type == 'NAF':
            return self.node.get('id')
        elif self.type == 'KAF':
            return self.node.get('oid')        
        
    def set_holder(self,hol):
        """
        Sets the opinion holder
        @type hol: L{Cholder}
        @param hol: the opinion holder
        """        
        self.node.append(hol.get_node())
        
    def get_holder(self):
        """
        Returns the opinion holder
        @rtype: L{Cholder}
        @return: the opinion holder
        """    
        node_hol = self.node.find('opinion_holder')
        if node_hol is not None:
            return Cholder(node_hol)
        else:
            return None

    def set_target(self,tar):
        """
        Sets the opinion target
        @type tar: L{Ctarget}
        @param tar: the opinion target
        """    
        self.node.append(tar.get_node())
        
    def get_target(self):
        """
        Returns the opinion target
        @rtype: L{Ctarget}
        @return: the opinion target
        """    
        node_target = self.node.find('opinion_target')
        if node_target is not None:
            return Ctarget(node_target)
        else:
            return None
        
    def set_expression(self,exp):
        """
        Sets the opinion expression
        @type exp: L{Cexpression}
        @param exp: the opinion expression
        """    
        self.node.append(exp.get_node())

    def get_expression(self):
        """
        Returns the opinion expression
        @rtype: L{Cexpression}
        @return: the opinion expression
        """  
        node_exp = self.node.find('opinion_expression')
        if node_exp is not None:
            return Cexpression(node_exp)
        else:
            return None
        
    def __str__(self):
        return dump(self.node)  
    
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
    
    



class Copinions:
    """
    This class encapsulates the opinion layer in KAF/NAF (set of opinions)
    """
    def __init__(self,node=None,type='NAF'):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        @type type: string
        @param type: the type of the object (KAF or NAF)
        """
        self.type = type
        if node is None:
            self.node = etree.Element('opinions')
        else:
            self.node = node
            
    def __get_opinion_nodes(self):
        for node in self.node.findall('opinion'):
            yield node
            
    def get_opinions(self):
        """
        Iterator that returns all the opinions in the layer
        @rtype: L{Copinion}
        @return: iterator for the opinions
        """
        for node in self.__get_opinion_nodes():
            yield Copinion(node,self.type)
            
    def to_kaf(self):
        """
        Converts the opinion layer to KAF
        """
        if self.type == 'NAF':
            for node in self.__get_opinion_nodes():
                node.set('oid',node.get('id'))
                del node.attrib['id']

    def to_naf(self):
        """
        Converts the opinion layer to NAF
        """
        if self.type == 'KAF':
            for node in self.__get_opinion_nodes():
                node.set('id',node.get('oid'))
                del node.attrib['oid']                
            
            
    def add_opinion(self,opi_obj):
        """
        Adds the opinion object to the layer
        @type opi_obj:  L{Copinion}
        @param opi_obj: the opinion object
        """ 
        self.node.append(opi_obj.get_node())
                         
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
        
    def remove_this_opinion(self,opinion_id):
        """
        Removes the opinion for the given opinion identifier
        @type opinion_id: string
        @param opinion_id: the opinion identifier to be removed
        """
        for opi in self.get_opinions():
            if opi.get_id() == opinion_id:
                self.node.remove(opi.get_node())
                break
                
