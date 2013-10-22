from lxml import etree

class target:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('target')
        else:
            self.node = node
            
    def get_id(self):
        return self.node.get('id')


class span:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('span')
        else:
            self.node = node
             
        #self.targets = []
        

    def __get_target_nodes(self):
        for target_node in self.node.findall('target'):
            yield target_node
    
    def __iter__(self):
        for target_node in self.__get_target_nodes():
            yield target(target_node)
                                            