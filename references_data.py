# Modified for NAF/KAf
from span_data import *

class Creferences:
    def __init__(self,node=None):
        self.type = 'NAF/KAF'
        if node is None:
            self.node = etree.Element('references')
        else:
            self.node = node
            
    def get_node(self):
        return self.node
    
    def __iter__(self):
        for span_node in self.node.findall('span'):
            yield Cspan(span_node)
            
    def add_span(self,term_span):
        new_span = Cspan()
        new_span.create_from_ids(term_span)
        self.node.append(new_span.get_node())

