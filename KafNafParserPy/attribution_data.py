"""
Parser for the attribution layer
"""

# Modified for KAF/NAF

from lxml import etree

from .span_data import Cspan
from .term_data import Cterm


class Cstatement:
    '''This class represents statements (main elements in attribution layer)'''

    def __init__(self, node=None, type='NAF'):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        @type type: string
        @param type: the type of the object (KAF or NAF)
        """
        self.type = type
        if node is None:
            self.node = etree.Element('statement')
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
        Returns the identifier of the statement element
        """
        return self.node.get('id')

    def set_id(self,this_id):
        """
        Sets the id of the element
        @type this_id: string
        @param this_id: the resource defining statement
        """
        self.node.set('id',this_id)

    def set_statement_target(self,starget):
        """
        Adds the target of the element
        @type starget: L{Cstatement_target}
        @param starget: the target of the statement
        """
        self.node.append(starget.get_node())


    def get_statement_target(self):
        """
        Retrieves the statement target
        @rtype: L{Cstatement_target}
        @return: statement target
        """
        return self.node.find('statement_target')

    def set_statement_source(self,ssource):
        """
        Adds the source of the element
        @type ssource: L{Cstatement_source}
        @param ssource: the source of the statement
        """
        self.node.append(ssource.get_node())

    def get_statement_source(self):
        """
        Retrieves the statement source
        @rtype: L{Cstatement_source}
        @return: statement source
        """
        return self.node.find('statement_source')

    def set_statement_cue(self,scue):
        """
        Adds the cue of the element
        @type scue: L{Cstatement_cue}
        @param scue: the cue of the statement
        """
        self.node.append(scue.get_node())

    def get_statement_cue(self):
        """
        Retrieves the statement cue
        @rtype: L{Cstatement_cue}
        @return: statement cue
        """
        return self.node.find('statement_cue')


class Cstatement_target:
    '''Represents the statement_target element'''

    def __init__(self, node=None, type='NAF'):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        @type type: string
        @param type: the type of the object (KAF or NAF)
        """
        self.type = type
        if node is None:
            self.node = etree.Element('statement_target')
        else:
            self.node = node

    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node

    def get_span(self):
        """
        Returns the span of the statement_target element
        @rtype: L{Cspan}
        @return: span object
        """
        span_obj = self.node.find('span')
        if span_obj is not None:
            return Cspan(span_obj)
        return None

    def set_span(self,my_span):
        """
        Sets the id of the element
        @type my_span: L{Cspan}
        @param my_span: the span of the statement_target
        """
        self.node.append(my_span.get_node())


class Cstatement_source:
    '''Represents the statement_source element'''

    def __init__(self, node=None, type='NAF'):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        @type type: string
        @param type: the type of the object (KAF or NAF)
        """
        self.type = type
        if node is None:
            self.node = etree.Element('statement_source')
        else:
            self.node = node

    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node

    def get_span(self):
        """
        Returns the span of the statement_source element
        @rtype: L{Cspan}
        @return: span object
        """
        span_obj = self.node.find('span')
        if span_obj is not None:
            return Cspan(span_obj)
        return None

    def set_span(self,my_span):
        """
        Sets the id of the element
        @type my_span: L{Cspan}
        @param my_span: the span of the statement_source
        """
        self.node.append(my_span.get_node())


class Cstatement_cue:
    '''Represents the statement_cue element'''

    def __init__(self, node=None, type='NAF'):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        @type type: string
        @param type: the type of the object (KAF or NAF)
        """
        self.type = type
        if node is None:
            self.node = etree.Element('statement_cue')
        else:
            self.node = node

    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node

    def get_span(self):
        """
        Returns the span of the statement_cue element
        @rtype: L{Cspan}
        @return: span object
        """
        span_obj = self.node.find('span')
        if span_obj is not None:
            return Cspan(span_obj)
        return None

    def set_span(self,my_span):
        """
        Sets the id of the element
        @type my_span: L{Cspan}
        @param my_span: the span of the statement_cue
        """
        self.node.append(my_span.get_node())


class Cattribution:
    '''This class represents the attribution layer'''

    def __init__(self, node=None, type='NAF'):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        @type type: string
        @param type: the type of the object (KAF or NAF)
        """
        self.idx = {}
        self.type = type
        if node is None:
            self.node = etree.Element('attribution')
        else:
            self.node = node
            for node_statement in self.__get_node_statements():
                statement_obj = Cstatement(node_statement, self.type)
                self.idx[statement_obj.get_id()] = node_statement

    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node

    def __get_node_statements(self):
        for node_statement in self.node.findall('statement'):
            yield node_statement

    def __iter__(self):
        """
        Iterator that returns single statement objects in the layer
        @rtype: L{Cterm}
        @return: term objects
        """
        for node_statement in self.__get_node_statements():
            yield Cterm(node_statement, self.type)

    def get_statement(self, statement_id):
        """
        Returns the statement object for the supplied identifier
        @type statement_id: string
        @param statement_id: statement identifier
        """
        if statement_id in self.idx:
            return Cstatement(self.idx[statement_id], self.type)
        else:
            return None

    def add_statement(self, statement_obj):
        """
        Adds a statement object to the layer
        @type statement_obj: L{Cstatement}
        @param statement_obj: the statement object
        """
        if statement_obj.get_id() in self.idx:
            raise ValueError("Statement with id {} already exists!"
                             .format(statement_obj.get_id()))
        self.node.append(statement_obj.get_node())
        self.idx[statement_obj.get_id()] = statement_obj


    def to_kaf(self):
        pass

    def to_naf(self):
        pass
