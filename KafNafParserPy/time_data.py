"""
Parser for time expressions (following timex) in KAF/NAF
"""

from __future__ import print_function

from lxml import etree

from .span_data import Cspan


class Ctime:
    """
    This class encapsulates a <timex> object in KAF/NAF
    """

    def __init__(self,node=None):
        """
        Constructor of the object
        @param node: this is the node of the element. If None it will create a new object.
        """
        if node is None:
            self.node = etree.Element('timex3')
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
        Returns the timex identifier
        @rtype: string
        @return: the timex identifier
        """
        return self.node.get('id')


    def set_id(self, i):
        """
        Sets the identifier for the timex
        @type i: string
        @param i: timex identifier
        """
        self.node.set('id',i)


    def get_type(self):
        """
        Returns the timex type
        @rtype: string
        @return: the timex type
        """
        return self.node.get('type')


    def set_type(self, t):
        """
        Sets the type for the timex
        @type t: string
        @param t: timex type
        """
        self.node.set('type',t)

    
    def set_timex_type(self, t):
        """
        Sets the type for the timex
        @type t: string
        @param t: timex type
        """
        self.node.set('type',t)

    def get_value(self):
        """
        Returns the timex value
        @rtype: string
        @return: the timex value
        """
        return self.node.get('value')


    def set_value(self, v):
        """
        Sets the value for the timex
        @type v: string
        @param v: timex value
        """
        self.node.set('value',v)

    def get_span(self):
        """
        Returns the span object of the timex
        @rtype: L{Cspan}
        @return: the timex span
        """
        node_span = self.node.find('span')
        if node_span is not None:
            return Cspan(node_span)
        else:
            return None
                            
    def set_span(self,this_span):
        """
        Sets the span for the timex
        @type this_span: L{Cspan}
        @param this_span: timex identifier
        """
        self.node.append(this_span.get_node())


    def get_functionInDocument(self):
        """
        Returns the timex functionInDocument
        @rtype: string
        @return: the timex functionInDocument
        """
        return self.node.get('functionInDocument')


    def set_functionInDocument(self, f):
        """
        Sets the functionInDocument for the timex
        @type f: string
        @param f: timex functionInDocument
        """
        self.node.set('functionInDocument',f)


    def get_beginPoint(self):
        """
        Returns the timex beginPoint
        @rtype: string
        @return: the timex beginPoint
        """
        return self.node.get('beginPoint')
        
        
    def set_beginPoint(self, bp):
        """
        Sets the beginPoint for the timex
        @type bp: string
        @param bp: timex beginPoint
        """
        self.node.set('beginPoint',bp)


    def get_endPoint(self):
        """
        Returns the timex endPoint
        @rtype: string
        @return: the timex endPoint
        """
        return self.node.get('endPoint')
        
        
    def set_endPoint(self, ep):
        """
        Sets the endPoint for the timex
        @type ep: string
        @param ep: timex endPoint
        """
        self.node.set('endPoint',ep)


    def get_quant(self):
        """
        Returns the timex quant
        @rtype: string
        @return: the timex quant
        """
        return self.node.get('quant')
        
        
    def set_quant(self, q):
        """
        Sets the quant for the timex
        @type q: string
        @param q: timex quant
        """
        self.node.set('quant',q)


    def get_freq(self):
        """
        Returns the timex freq
        @rtype: string
        @return: the timex freq
        """
        return self.node.get('freq')
        
        
    def set_freq(self, f):
        """
        Sets the freq for the timex
        @type f: string
        @param f: timex freq
        """
        self.node.set('freq',f)


    def get_temporalFunction(self):
        """
        Returns the timex temporalFunction
        @rtype: string
        @return: the timex temporalFunction
        """
        return self.node.get('temporalFunction')
        
        
    def set_temporalFunction(self, tf):
        """
        Sets the temporalFunction for the timex
        @type tf: string
        @param tf: timex temporalFunction
        """
        self.node.set('temporalFunction',tf)


    def get_valueFromFunction(self):
        """
        Returns the timex valueFromFunction
        @rtype: string
        @return: the timex valueFromFunction
        """
        return self.node.get('valueFromFunction')
        
        
    def set_valueFromFunction(self, v):
        """
        Sets the valueFromFunction for the timex
        @type v: string
        @param v: timex valueFromFunction
        """
        self.node.set('valueFromFunction',v)

    def get_mod(self):
        """
        Returns the timex mod
        @rtype: string
        @return: the timex mod
        """
        return self.node.get('mod')
        
        
    def set_mod(self, m):
        """
        Sets the mod for the timex
        @type m: string
        @param m: timex mod
        """
        self.node.set('mod',m)


    def get_anchorTimeID(self):
        """
        Returns the timex anchorTimeID
        @rtype: string
        @return: the timex anchorTimeID
        """
        return self.node.get('anchorTimeID')
        
        
    def set_anchorTimeID(self, ati):
        """
        Sets the anchorTimeID for the timex
        @type ati: string
        @param ati: timex anchorTimeID
        """
        self.node.set('anchorTimeID',ati)


    def get_comment(self):
        """
        Returns the timex comment
        @rtype: string
        @return: the timex comment
        """
        return self.node.get('comment')
        
        
    def set_comment(self, c):
        """
        Sets the comment for the timex
        @type c: string
        @param c: timex comment
        """
        self.node.set('comment',c)




class CtimeExpressions:
    """
    This class encapsulates the timeExpressions layer (collection of timex3 objects)
    """

    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create an empty one)
        @param node: this is the node of the element. If it is None, a new element will be created.
        """
        self.idx = {}
        if node is None:
            self.node = etree.Element('timeExpressions')
        else:
            self.node = node
            for node_timex in self.__get_node_timex3s():
                timex_obj = Ctime(node_timex)
                self.idx[timex_obj.get_id()] = node_timex



    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node


    def __get_node_timex3s(self):
        for node_timex in self.node.findall('timex3'):
            yield node_timex

                
    def __iter__(self):
        """
        Iterator that returns single timex objects in the layer
        @rtype: L{Ctime}
        @return: timex objects
        """
        for node_timex in self.__get_node_timex3s():
            yield Ctime(node_timex)


    def get_timex(self, timex_id):
        """
        Returns the timex object for the supplied identifier
        @type timex_id: string
        @param timex_id: timex identifier
        """
        if timex_id in self.idx:
            return Ctime(self.idx[timex_id])
        else:
            return None

    def get_timeExpressions(self):
        """
        Iterator to get the timex objects
        @rtype: L{Ctime}
        @return: iterator for getting the timex object
        """
        for node_pre in self.node.findall('timex3'):
            yield Ctime(node_pre)


    def add_timex(self, timex_obj):
        """
        Adds a timex object to the layer.
        @type timex_obj: L{Ctime}
        @param timex_obj: the timex object
        """
        timex_id = timex_obj.get_id()
        #check if id is not already present
        if not timex_id in self.idx:
            
            timex_node = timex_obj.get_node()
            self.node.append(timex_node)
            self.idx[timex_id] = timex_node
        else:
            #FIXME: what we want is that the element receives a new identifier that
            #is not present in current element yet
            print('Error: trying to add new element with existing identifier')


    def remove_timex3s(self, list_timex_ids):
        """
        Removes a list of terms from the layer
        @type list_timex_ids: list (of strings)
        @param list_timex_ids: list of timex identifier to be removed
        """
        nodes_to_remove = set()
        for timex in self:
            if timex.get_id() in list_timex_ids:
                nodes_to_remove.add(timex.get_node())
                #for removing the previous comment (expected the layer will look like termlayer)
                prv = timex.get_node().getprevious()
                if prv is not None:
                    nodes_to_remove.add(prv)

        for node in nodes_to_remove:
            self.node.remove(node)
