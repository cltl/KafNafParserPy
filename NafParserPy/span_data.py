
class span:
    def __init__(self,node):
        self.targets = []
        if node is not None:
            for target_node in node.findall('target'):
                self.targets.append(target_node.get('id'))
    
    def __str__(self):
        s = ' '.join(self.targets)
        return s
    
    def __iter__(self):
        for target in self.targets:
            yield target
                                            