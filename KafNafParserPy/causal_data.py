"""
Parser for the clink layer in KAF/NAF
"""
from lxml import etree

class Cclink:
    """
    This class encapsulates a clink object in KAF/NAF
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node: this is the node of the element.
            If it is None it will create a new object
        """
        if node is None:
            self.node = etree.Element('clink')
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

    def get_id(self):
        """
        Returns the token identifier
        @rtype: string
        @return: the token identifier
        """
        return self.node.get('id')


    def get_from(self):
        """
        Returns the from attribute of the clink
        @rtype: string
        @return: the from attribute
        """
        return self.node.get('from')

    def get_to(self):
        """
        Returns the to attribute of the clink
        @rtype: string
        @return: the to attribute
        """
        return self.node.get('to')

    def set_id(self,this_id):
        """
        Set the identifier for the token
        @type this_id: string
        @param this_id: the identifier
        """
        return self.node.set('id',this_id)

    def set_from(self, f):
        """
        Sets the from attribute
        @type f: string
        @param f: the from attribute
        """
        self.node.set('from',f)

    def set_to(self,t):
        """
        Sets the to attribute
        @type t: string
        @param t: the to attribute
        """
        self.node.set('to',t)

    def set_comment(self,c):
        """
        Sets the XML comment for the clink
        @type c: string
        @param c: the string comment
        """
        c = c.replace('--','- -')
        self.node.insert(0,etree.Comment(c))

    def __str__(self):
        return dump(self.node)

class CcausalRelations:
    """
    This class encapsulates the clink layer in KAF/NAF
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node: this is the node of the element.
            If it is None it will create a new object
        """
        if node is None:
            self.node = etree.Element('causalRelations')
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


    def __get_node_causalRelations(self):
        for node_clink in self.node.findall('clink'):
            yield node_clink

    def get_clinks(self):
        """
        Iterator that returns all the causalRelations in the layer
        @rtype: L{Cclink}
        @return: list of causalRelations (iterator)
        """
        for node in self.__get_node_causalRelations():
            yield Cclink(node)

    def add_clink(self,my_clink):
        """
        Adds a clink object to the layer
        @type my_clink: L{Cclink}
        @param my_clink: the clink object to be added
        """
        self.node.append(my_clink.get_node())

    def remove_this_clink(self,clink_id):
        """
        Removes the clink for the given clink identifier
        @type clink_id: string
        @param clink_id: the clink identifier to be removed
        """
        for clink in self.get_clinks():
            if clink.get_id() == clink_id:
                self.node.remove(clink.get_node())
                break
