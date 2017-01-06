"""
Parser for the factvalue layer in KAF/NAF
"""

from lxml import etree

from .span_data import *


class Cfactval:

    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        self.type = 'NAF/KAF'
        if node is None:
            self.node = etree.Element('factVal')
        else:
            self.node = node

    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node

    def get_resource(self):
        """
        Returns the resource that defines the factuality value
        @return: resource name
        @rtype: string
        """
        return self.node.get('resource')

    def set_resource(self,r):
        """
        Sets the resource that defines the factuality value
        @type r: string
        @param r: the resource defining factuality
        """
        self.node.set('resource',r)


    def get_value(self):
        """
        Returns the value of the factVal element
        @return: factuality value
        @rtype: string
        """
        return self.node.get('value')

    def set_value(self,v):
        """
        Sets the value for the factVal element
        @type v: string
        @param v: the value for the element
        """
        self.node.set('value',v)

    def get_confidence(self):
        """
        Returns the confidence of the factVal element
        @return: confidence value
        @rtype: string
        """
        return self.node.get('confidence')


    def set_confidence(self,c):
        """
        Sets confidence for the factVal element
        @type c: string
        @param c: the value for the element
        """
        self.node.set('confidence',c)
    
    def get_source(self):
        """
        Returns the source of the factVal element
        @return: source of annotation
        @rtype: string
        """
        return self.node.get('source')


    def set_source(self,s):
        """
        Sets source for the factVal element
        @type s: string
        @param s: the source of the element
        """
        self.node.set('source',s)

class Cfactuality:

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
            self.node = etree.Element('factuality')
        else:
            self.node = node

    def get_node(self):
        """
        Returns the node
        """
        return self.node


    def get_id(self):
        """
        Returns the identifier of the factuality element
        """
        return self.node.get('id')

    def set_id(self,this_id):
        """
        Sets the id of the element
        @type this_id: string
        @param this_id: the resource defining factuality
        """
        self.node.set('id',this_id)


    def get_span(self):
        """
        Returns the span of the factuality element
        @type my_span: L{Cspan}
        @param my_span: span object
        """
        span_obj = self.node.find('span')
        if span_obj is not None:
            return Cspan(span_obj)
        return None

    def set_span(self,my_span):
        """
        Sets the id of the element
        @type this_id: L{Cspan}
        @param this_id: the resource defining factuality
        """
        self.node.append(my_span.get_node())

    def add_factval(self,fval):
        """
        Sets the id of the element
        @type this_id: L{Cspan}
        @param this_id: the resource defining factuality
        """
        self.node.append(fval.get_node())

    #copy of function add_factval with expected name
    def add_factVal(self,fval):
        """
        Sets the id of the element
        @type this_id: L{Cspan}
        @param this_id: the resource defining factuality
        """
        self.node.append(fval.get_node())


    def get_factVals(self):
        """
        Iterator to get the factuality values
        @rtype: L{Cfactuality}
        @return: iterator for getting the factuality's value objects
        """
        for node_pre in self.node.findall('factVal'):
            yield Cfactval(node_pre)


class Cfactualities:
    """
    This class represents the new factuality layer
    """
    def __init__(self,node=None,type='NAF'):
        """
        Constructor of the object
        @type node: xml ELement or None (to create an empty one)
        @param node: this is the node of the element. If it is None it will create a new object
        @type type: string
        @param type: the type of the object (KAF or NAF), NAF is default
        """
        self.type = type
        if node is None:
            self.node = etree.Element('factualities')
        else:
            self.node = node

    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node


    def add_factuality(self, factval):
        """
        Adds a factuality element to the layer
        """
        self.node.append(factval.get_node())
    
    
    
    def remove_this_factuality(self,factuality_id):
        """
        Removes the factuality for the given factuality identifier
        @type factuality_id: string
        @param factuality_id: the factuality identifier to be removed
        """
        for fact in self.get_factualities():
            if fact.get_id() == factuality_id:
                self.node.remove(fact.get_node())
                break
    
       
    def remove_factuality(self, fid):
        """
        Removes a factuality element with a specific id from the layer
        """
        for node_pre in self.node.findall('factuality'):
            if node_pre.get('id') == fid:
                self.node.remove(node_pre)


    def get_factualities(self):
        """
        Iterator to get the factualities
        @rtype: L{Cfactuality}
        @return: iterator for getting the factuality objects
        """
        for node_pre in self.node.findall('factuality'):
            yield Cfactuality(node_pre)

    def to_kaf(self):
        pass

    def to_naf(self):
        pass

    def __str__(self):
        return dump(self.node)





class Cfactvalue:
    """
    This class encapsulates a factvalue object in KAF/NAF (old version)
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node: this is the node of the element.
            If it is None it will create a new object
        """
        if node is None:
            self.node = etree.Element('factvalue')
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
        Returns the fact identifier
        @rtype: string
        @return: the fact identifier
        """
        return self.node.get('id')

    def get_prediction(self):
        """
        Returns the prediction attribute of the factvalue
        @rtype: string
        @return: the prediction attribute
        """
        return self.node.get('prediction')

    def get_confidence(self):
        """
        Returns the confidence of the element
        @rtype: string
        @return: the confidence of the element
        """
        return self.node.get('confidence')

    def set_id(self,this_id):
        """
        Set the identifier for the fact
        @type this_id: string
        @param this_id: the identifier
        """
        return self.node.set('id',this_id)

    def set_prediction(self,prediction):
        """
        Sets the prediction attribute
        @type prediction: string
        @param prediction: the prediction attribute
        """
        self.node.set('prediction',prediction)

    def set_confidence(self,confidence):
        """
        Sets the confidence attribute
        @type confidence: string
        @param confidence: the confidence attribute
        """
        self.node.set('confidence',confidence)

    def __str__(self):
        return dump(self.node)

class Cfactualitylayer:
    """
    This class encapsulates the factvalue layer in KAF/NAF (old version)
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node: this is the node of the element.
            If it is None it will create a new object
        """
        if node is None:
            self.node = etree.Element('factualitylayer')
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

    def __str__(self):
        return dump(self.node)

    def __get_factvalue_nodes(self):
        for node_factvalue in self.node.findall('factvalue'):
            yield node_factvalue

    def get_factvalues(self):
        """
        Iterator that returns all the factualitylayer in the layer
        @rtype: L{Cfactvalue}
        @return: list of factualitylayer (iterator)
        """
        for node in self.__get_factvalue_nodes():
            yield Cfactvalue(node)

    def add_factvalue(self,my_factvalue):
        """
        Adds a factvalue object to the layer
        @type my_factvalue: L{Cfactvalue}
        @param my_factvalue: the factvalue object to be added
        """
        self.node.append(my_factvalue.get_node())

    def remove_this_factvalue(self,factvalue_id):
        """
        Removes the factvalue for the given factvalue identifier
        @type factvalue_id: string
        @param factvalue_id: the factvalue identifier to be removed
        """
        for fact in self.get_factvalues():
            if fact.get_id() == factvalue_id:
                self.node.remove(fact.get_node())
                break
