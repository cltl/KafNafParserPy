
class wf:
    def __init__(self,node):
        self.id = ''
        self.sent = ''
        self.para = ''
        self.page = ''
        self.offset = ''
        self.lenght = ''
        self.xpath = ''
        self.text = ''
        if node is not None:
            self.id = node.get('id','')
            self.sent = node.get('sent','')
            self.para = node.get('para','')
            self.page = node.get('page','')
            self.offset = node.get('offset','')
            self.lenght = node.get('lenght','')
            self.xpath = node.get('xpath','')
            self.text = node.text
    def __str__(self):
        s = 'WF:  '
        s += 'Id: '+self.id+'  Text:'+self.text+'  Sent:'+self.sent+'  Para:'+self.para+'  Page:'+self.page+'  Offset:'+self.offset+'  Length'+self.lenght+'  xpath:'+self.xpath+'\n'
        return s

    def get_id(self):
        return self.id
    
    def get_text(self):
        return self.text
    
    def get_sent(self):
        return self.sent
    
class text:
    def __init__(self,node):
        self.wfs = []
        self.idx_id_to_obj = {}
        if node is not None:
            for wfnode in node.findall('wf'):
                self.wfs.append(wf(wfnode))
                this_id = self.wfs[-1].get_id()
                this_pos = len(self.wfs)-1
                self.idx_id_to_obj[this_id]=this_pos
    
    def __iter__(self):
        for wf in self.wfs:
            yield wf
            
    def get_wf(self,tokenid):
        wf_position = self.idx_id_to_obj.get(tokenid,None)
        if wf_position is not None:
            return self.wfs[wf_position]
        else:
            return None
            
    def __str__(self):
        s = 'Text:\n'
        for wf in self.wfs:
            s+=str(wf)
        s += '\n'
        return s
    
    
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
                