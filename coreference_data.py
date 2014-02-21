from lxml import etree
from span_data import Cspan

class Ccoreference:
    def __init__(self,node=None,type='NAF'):
        self.type = type
        if node is None:
            self.node = etree.Element('coref')
        else:
            self.node = node
            
    def get_id(self):
        if self.type == 'NAF':
            return self.node.get('id')
        elif self.type == 'KAF':
            return self.node.get('coid')
    
    def get_spans(self):
        for node_span in self.node.findall('span'):
            yield Cspan(node_span)
    
            

class Ccoreferences:
    def __init__(self,node=None, type='NAF'):
        self.type = type
        if node is None:
            self.node = etree.Element('coreferences')
        else:
            self.node = node
            
    def __get_corefs_nodes(self):
        for coref_node in self.node.findall('coref'):
            yield coref_node
            
    def get_corefs(self):
        for coref_node in self.__get_corefs_nodes():
            yield Ccoreference(coref_node,self.type)
            
    def to_kaf(self):
        if self.type == 'NAF':
            for node_coref in self.__get_corefs_nodes():
                node_coref.set('coid',node_coref.get('id'))
                del node_coref.attrib['id']
        
    def to_naf(self):
        if self.type == 'KAF':
            for node_coref in self.__get_corefs_nodes():
                node_coref.set('id',node_coref.get('coid'))
                del node_coref.attrib['coid']
                    
            