"""
This modules parses the text layer of a KAF or NAF file
"""
from lxml import etree


class Cwf:
    """
    This class represents a single token (NAF/KAF wf object)
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
        ##self.id = ''    self.sent = ''      self.para = ''      self.page = ''      self.offset = ''      self.lenght = '' s
        if node is None:
            self.node = etree.Element('wf')
        else:
            self.node = node

    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
    
    def set_id(self,this_id):
        """
        Set the identifier for the token
        @type this_id: string
        @param this_id: the identifier
        """
        if self.type == 'NAF':
            return self.node.set('id',this_id)
        elif self.type == 'KAF':
            return self.node.set('wid',this_id)
                
    def get_id(self):
        """
        Returns the token identifier
        @rtype: string
        @return: the token identifier
        """
        if self.type == 'NAF':
            return self.node.get('id')
        elif self.type == 'KAF':
            return self.node.get('wid')
    
    def set_text(self,this_text):
        """
        Set the text for the token
        @type this_text: string
        @param this_text: the text
        """
        self.node.text = this_text
        
    def get_text(self):
        """
        Returns the text of the token
        @rtype: string
        @return: text of the token
        """
        return self.node.text
    
    def set_sent(self,this_sent):
        """
        Set the sentence for the token
        @type this_sent: string
        @param this_sent: the sentence identifier
        """
        self.node.set('sent',this_sent)
        
    def get_sent(self):
        """
        Returns the sentence of the token
        @rtype: string
        @return: sentence of the token
        """
        return self.node.get('sent')
    
    def get_offset(self):
        """
        Returns the offset of the token
        @rtype: string
        @return: the offset
        """
        return self.node.get('offset')
    

    def set_offset(self,offset):
        """
        Set the offset for the token
        @type offset: string
        @param offset: the offset
        """
        self.node.set('offset',o)

    def get_length(self):
        """
        Returns the length of the token
        @rtype: string
        @return: the length
        """
        return self.node.get('length')
    

    def set_length(self,length):
        """
        Set the length for the token
        @type length: string
        @param length: the length
        """
        self.node.set('length',o)
        
    def set_para(self,p):
        """
        Set the paragraph for the token
        @type p: string
        @param p: the paragraph identifier
        """
        self.node.set('para',p)
    
    
class Ctext:
    """
    This class encapsulates the text layer
    """
    def __init__(self,node=None,type='NAF'):
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
            self.node = etree.Element('text')
        else:
            self.node = node
            for wf_node in self.__get_wf_nodes():
                if self.type == 'NAF': label_id = 'id'
                elif self.type == 'KAF': label_id = 'wid'
                self.idx[wf_node.get(label_id)] = wf_node
                
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
            for node in self.__get_wf_nodes():
                node.set('wid',node.get('id'))
                del node.attrib['id']

    def to_naf(self):
        """
        Converts the object to NAF
        """
        if self.type == 'KAF':
            self.type = 'NAF'
            for node in self.__get_wf_nodes():
                node.set('id',node.get('wid'))
                del node.attrib['wid']

    def __get_wf_nodes(self):
        for wf_node in self.node.findall('wf'):
            yield wf_node
            
    def __iter__(self):
        """
        Iterator that returns all the tokens
        @rtype: L{Cwf}
        @return: single token objects
        """
        for wf_node in self.__get_wf_nodes():
            yield Cwf(node=wf_node,type=self.type)
            
    def get_wf(self,token_id):
        """
        Returns the token object for the given token identifier
        @type token_id: string
        @param token_id: the token identifier
        @rtype: L{Cwf}
        @return: the token object
        """  
        wf_node = self.idx.get(token_id)
        if wf_node is not None:
            return Cwf(node=wf_node,type=self.type)
        else:
            return None
    
    def add_wf(self,wf_obj):
        """
        Adds a token object to the text layer
        @type wf_obj: L{Cwf}
        @param wf_obj: token object
        """
        self.node.append(wf_obj.get_node())
        
    
    def remove_tokens_of_sentence(self,sentence_id):
        """
        Removes the tokens of the given sentence
        @type sentence_id: string
        @param sentence_id: the sentence identifier  
        """
        nodes_to_remove = set()
        for wf in self:
            if wf.get_sent() == sentence_id:
                nodes_to_remove.add(wf.get_node())
        
        for node in nodes_to_remove:
            self.node.remove(node)    
        
