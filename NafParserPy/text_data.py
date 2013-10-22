from lxml import etree

class wf:
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
    
class text:
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
            yield wf(wf_node)
            
    def get_wf(self,token_id):
        wf_node = self.idx.get(token_id)
        if wf_node is not None:
            return wf(wf_node)
        else:
            return None
        
   
    
if __name__ == '__main__':
    from lxml import etree
    data = '''<text>
                <wf id="w1" offset="0" length="4" sent="1" para="1">John</wf>
                <wf id="w2" offset="5" length="6" sent="1" para="1">taught</wf>
                <wf id="w3" offset="12" length="11" sent="1" para="1">mathematics</wf>
                <wf id="w4" offset="24" length="2" sent="1" para="1">20</wf>
                <wf id="w5" offset="27" length="7" sent="1" para="1">minutes</wf>
                <wf id="w6" offset="35" length="5" sent="1" para="1">every</wf>
                <wf id="w7" offset="41" length="6" sent="1" para="1">Monday</wf>
                <wf id="w8" offset="48" length="2" sent="1" para="1">in</wf>
                <wf id="w9" offset="51" length="3" sent="1" para="1">New</wf>
                <wf id="w10" offset="55" length="3" sent="1" para="1">York</wf>
                <wf id="w11" offset="59" length="1" sent="1" para="1">.</wf>
                <wf id="w12" offset="62" length="2" sent="2" para="2">He</wf>
                <wf id="w13" offset="65" length="5" sent="2" para="2">liked</wf>
                <wf id="w14" offset="71" length="2" sent="2" para="2">it</wf>
                <wf id="w15" offset="74" length="1" sent="2" para="2">a</wf>
                <wf id="w16" offset="76" length="3" sent="2" para="2">lot</wf>
                <wf id="w17" offset="80" length="1" sent="2" para="2">!</wf>
                </text>'''
    node = etree.fromstring(data, parser=None, base_url=None)
    obj = text(node)
    print obj
                