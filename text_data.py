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


    def get_id(self):
        if self.type == 'NAF':
            return self.node.get('id')
        elif self.type == 'KAF':
            return self.node.get('wid')
    
    def get_text(self):
        return self.node.text
    
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
        