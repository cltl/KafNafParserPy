# included code for NAF/KAF

from lxml import etree


class Cwf:
    def __init__(self,node=None,type='NAF'):
        self.type = type
        ##self.id = ''    self.sent = ''      self.para = ''      self.page = ''      self.offset = ''      self.lenght = '' s
        if node is None:
            self.node = etree.Element('wf')
        else:
            self.node = node

    def get_node(self):
        return self.node
    
    def set_id(self,this_id):
        if self.type == 'NAF':
            return self.node.set('id',this_id)
        elif self.type == 'KAF':
            return self.node.set('wid',this_id)
                
    def get_id(self):
        if self.type == 'NAF':
            return self.node.get('id')
        elif self.type == 'KAF':
            return self.node.get('wid')
    
    def set_text(self,this_text):
        self.node.text = this_text
        
    def get_text(self):
        return self.node.text
    
    def set_sent(self,this_sent):
        self.node.set('sent',this_sent)
        
    def get_sent(self):
        return self.node.get('sent')
    
    
class Ctext:
    def __init__(self,node=None,type='NAF'):
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
        return self.node
    
    def to_kaf(self):
        if self.type == 'NAF':
            self.type = 'KAF'
            for node in self.__get_wf_nodes():
                node.set('wid',node.get('id'))
                del node.attrib['id']

    def to_naf(self):
        if self.type == 'KAF':
            self.type = 'NAF'
            for node in self.__get_wf_nodes():
                node.set('id',node.get('wid'))
                del node.attrib['wid']

    def __get_wf_nodes(self):
        for wf_node in self.node.findall('wf'):
            yield wf_node
            
    def __iter__(self):
        for wf_node in self.__get_wf_nodes():
            yield Cwf(node=wf_node,type=self.type)
            
    def get_wf(self,token_id):
        wf_node = self.idx.get(token_id)
        if wf_node is not None:
            return Cwf(node=wf_node,type=self.type)
        else:
            return None
    
    def add_wf(self,wf_obj):
        self.node.append(wf_obj.get_node())
        
    def remove_tokens_of_sentence(self,sentence_id):
        nodes_to_remove = set()
        for wf in self:
            if wf.get_sent() == sentence_id:
                nodes_to_remove.add(wf.get_node())
        
        for node in nodes_to_remove:
            self.node.remove(node)    
        