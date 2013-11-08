from lxml import etree

class Cwf:
    def __init__(self,node=None):
        ##self.id = ''    self.sent = ''      self.para = ''      self.page = ''      self.offset = ''      self.lenght = '' s
        if node is None:
            self.node = etree.Element('wf')
        else:
            self.node = node


    def get_id(self):
        return self.node.get('id')
    
    def get_text(self):
        return self.node.text
    
    def get_sent(self):
        return self.node.get('sent')
    
class Ctext:
    def __init__(self,node=None):
        self.idx = {}
        if node is None:
            self.node = etree.Element('text')
        else:
            self.node = node
            for wf_node in self.__get_wf_nodes():
                self.idx[wf_node.get('id')] = wf_node
                
    def __get_wf_nodes(self):
        for wf_node in self.node.findall('wf'):
            yield wf_node
            
    def __iter__(self):
        for wf_node in self.__get_wf_nodes():
            yield Cwf(wf_node)
            
    def get_wf(self,token_id):
        wf_node = self.idx.get(token_id)
        if wf_node is not None:
            return Cwf(wf_node)
        else:
            return None
        