from span_data import *

class Creferences:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('references')
        else:
            self.node = node
            
    def __iter__(self):
        for span_node in self.node.findall('span'):
            yield Cspan(span_node)

