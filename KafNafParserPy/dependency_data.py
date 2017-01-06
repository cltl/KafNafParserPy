"""
Parser for the dependency layer in KAF/NAF
"""
from lxml import etree
#from lxml.objectify import dump


class Cdependency:
    """
    This class encapsulates a dependency object in KAF/NAF
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        if node is None:
            self.node = etree.Element('dep')
        else:
            self.node = node
            
    def get_node_comment(self):
        """
        Returns the lxml element for the comment
        @rtype: lxml Element
        @return: the lxml element for the comment
        """
        return self.node_comment
    
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
    
    def get_from(self):
        """
        Returns the from attribute of the dependency
        @rtype: string
        @return: the from attribute
        """
        return self.node.get('from')

    def set_from(self, f):
        """
        Sets the from attribute
        @type f: string
        @param f: the from attribute
        """
        self.node.set('from',f)

    def get_to(self):
        """
        Returns the to attribute of the dependency
        @rtype: string
        @return: the to attribute
        """
        return self.node.get('to')

    def set_to(self,t):
        """
        Sets the to attribute
        @type t: string
        @param t: the to attribute
        """
        self.node.set('to',t)
    
    def set_function(self,f):
        """
        Sets the function attribute
        @type f: string
        @param f: the function attribute
        """
        self.node.set('rfunc',f)

    def get_function(self):
        """
        Returns the function attribute of the dependency
        @rtype: string
        @return: the function attribute
        """
        return self.node.get('rfunc')

    def set_case(self,c):
        """
        Sets the case attribute
        @type c: string
        @param c: the case attribute
        """
        self.node.set('case',c)

    def get_case(self):
        """
        Returns the case attribute of the dependency
        @rtype: string
        @return: the case attribute
        """
        return self.node.get('case')

    def set_comment(self,c):
        """
        Sets the XML comment for the dependency
        @type c: string
        @param c: the string comment
        """
        c = c.replace('--','- -')
        self.node.insert(0,etree.Comment(c) )
            
    
    def __str__(self):
        return dump(self.node)



class Cdependencies:
    """
    This class encapsulates the dependency layer in KAF/NAF
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        if node is None:
            self.node = etree.Element('deps')
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


    def __get_node_deps(self):
        for node_dep in self.node.findall('dep'):
            yield node_dep
            
    def get_dependencies(self):
        """
        Iterator that returns all the dependencies in the layer
        @rtype: L{Cdependency}
        @return: list of dependencies (iterator)
        """
        for node in self.__get_node_deps():
            yield Cdependency(node)
            
            
    def add_dependency(self,my_dep):
        """
        Adds a dependency object to the layer
        @type my_dep: L{Cdependency}
        @param my_dep: the dependency object to be added
        """
        self.node.append(my_dep.get_node())
            