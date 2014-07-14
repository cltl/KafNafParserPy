"""
Parser for the span element
"""

# Modified for KAF/NAF

from lxml import etree
from lxml.objectify import dump

class Ctarget:
    """
    This class encapsulates the target element within a span object
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        self.type = 'NAF/KAF'
        if node is None:
            self.node = etree.Element('target')
        else:
            self.node = node
            
    def get_id(self):
        """
        Returns the id of the element
        @rtype: string
        @return: the id of the element
        """
        return self.node.get('id')
    
    def set_id(self,this_id):
        """
        Set the id of the element
        @type this_id: string
        @param this_id: the id for the element
        """
        self.node.set('id',this_id)
        
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node


class Cspan:
    """
    This class encapsulates a span object in KAF/NAF
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        self.type = 'NAF/KAF'
        if node is None:
            self.node = etree.Element('span')
        else:
            self.node = node
             
    def add_target_id(self,this_id):
        """
        Adds a new target to the span with the specified id
        @type this_id: string
        @param this_id: the id of the new target
        """
        new_target = Ctarget()
        new_target.set_id(this_id)
        self.node.append(new_target.get_node())
             
    def create_from_ids(self,list_ids):
        """
        Adds new targets to the span with the specified ids
        @type list_ids: list
        @param list_ids: list of identifiers
        """
        for this_id in list_ids:
            new_target = Ctarget()
            new_target.set_id(this_id)
            self.node.append(new_target.get_node())
            
    def add_target(self,target):
        """
        Adds a target object to the span
        @type target: L{Ctarget}
        @param target: target object
        """
        self.node.append(target.get_node())
                   

    def __get_target_nodes(self):
        for target_node in self.node.findall('target'):
            yield target_node
    
    def __iter__(self):
        """
        Iterator taht returns the target objects
        @rtype: L{Ctarget}
        @return: list of target objects (iterator)
        """
        for target_node in self.__get_target_nodes():
            yield Ctarget(target_node)
            
    def get_span_ids(self):
        """
        Returns the list of target ids for the span
        @rtype: list
        @return: list of target ids
        """
        return [t_obj.get_id() for t_obj in self]
    
    def __str__(self):
        return dump(self.node)
    
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
                                            