from lxml import etree
from lxml.objectify import dump

class Ctarget:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('target')
        else:
            self.node = node
            
    def get_id(self):
        return self.node.get('id')
    
    def set_id(self,this_id):
        self.node.set('id',this_id)
        
    def get_node(self):
        return self.node


class Cspan:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('span')
        else:
            self.node = node
             
             
    def create_from_ids(self,list_ids):
        for this_id in list_ids:
            new_target = Ctarget()
            new_target.set_id(this_id)
            self.node.append(new_target.get_node())
                   

    def __get_target_nodes(self):
        for target_node in self.node.findall('target'):
            yield target_node
    
    def __iter__(self):
        for target_node in self.__get_target_nodes():
            yield Ctarget(target_node)
            
    def get_span_ids(self):
        return [t_obj.get_id() for t_obj in self]
    
    def __str__(self):
        return dump(self.node)
    
    def get_node(self):
        return self.node
                                            