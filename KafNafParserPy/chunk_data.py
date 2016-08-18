"""
This module parses the chunk layer of a KAF/NAF object
"""
from __future__ import print_function

from lxml import etree

from .span_data import *


class Cchunk:
    """
    This class encapsulates a <chunk> NAF or KAF object
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
            self.node = etree.Element('chunk')
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
        Returns the chunk identifier
        @rtype: string
        @return: the chunk identifier
        """
        if self.type == 'NAF':
            return self.node.get('id')
        elif self.type == 'KAF':
            return self.node.get('cid')

    def set_id(self, i):
        """
        Sets the identifier for the chunk
        @type i: string
        @param i: chunk identifier
        """
        if self.type == 'NAF':
            self.node.set('id', i)
        elif self.type == 'KAF':
            self.node.set('cid', i)

    def get_head(self):
        """
        Returns the head of the chunk
        @rtype: string
        @return: the chunk head
        """
        return self.node.get('head')

    def set_head(self,h):
        """
        Sets the head for the chunk
        @type h: string
        @param h: term identifier of head
        """
        self.node.set('head',h)

    def get_phrase(self):
        """
        Returns the phrase type of the chunk
        @rtype: string
        @return: the chunk's phrase type
        """
        return self.node.get('phrase')

    def set_head(self,p):
        """
        Sets the phrase type for the chunk
        @type p: string
        @param p: phrase label
        """
        self.node.set('phrase',p)

    def get_span(self):
        """
        Returns the span object of the chunk
        @rtype: L{Cspan}
        @return: the chunk span
        """
        node_span = self.node.find('span')
        if node_span is not None:
            return Cspan(node_span)
        else:
            return None

    def set_span(self, this_span):
        """
        Sets the span for the chunk
        @type this_span: L{Cspan}
        @param this_span: chunk identifier
        """
        self.node.append(this_span.get_node())

class Cchunks:
    """
    This class encapsulates the chunk layer (collection of chunk objects)
    """

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
            self.node = etree.Element('chunks')
        else:
            self.node = node
            for node_chunk in self.__get_node_chunks():
                chunk_obj = Cchunk(node_chunk, self.type)
                self.idx[chunk_obj.get_id()] = node_chunk

    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node

    def to_kaf(self):
        """
        Converts the object to KAF (if it is NAF)
        """
        if self.type == 'NAF':
            self.type = 'KAF'
            for node in self.__get_node_terms():
                node.set('cid', node.get('id'))
                del node.attrib['id']

    def to_naf(self):
        """
        Converts the object to NAF (if it is KAF)
        """
        if self.type == 'KAF':
            self.type = 'NAF'
            for node in self.__get_node_terms():
                node.set('id', node.get('cid'))
                del node.attrib['cid']

    def __get_node_chunks(self):
        for node_chunk in self.node.findall('chunk'):
            yield node_chunk

    def __iter__(self):
        """
        Iterator that returns single chunk objects in the layer
        @rtype: L{Cchunk}
        @return: chunk objects
        """
        for node_chunk in self.__get_node_chunks():
            yield Cchunk(node_chunk, self.type)

    def get_chunk(self, chunk_id):
        """
        Returns the chunk object for the supplied identifier
        @type chunk_id: string
        @param chunk_id: chunk identifier
        """
        if chunk_id in self.idx:
            return Cchunk(self.idx[term_id], self.type)
        else:
            return None

    def add_chunk(self, chunk_obj):
        """
        Adds a chunk object to the layer
        @type chunk_obj: L{Cchunk}
        @param chunk_obj: the chunk object
        """
        if chunk_obj.get_id() in self.idx:
            raise ValueError("Chunk with id {} already exists!"
                             .format(chunk_obj.get_id()))
        self.node.append(chunk_obj.get_node())
        self.idx[chunk_obj.get_id()] = chunk_obj
