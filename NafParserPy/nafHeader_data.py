from lxml import etree
import time

class fileDesc:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('fileDesc')
        else:
            self.node = node
    
    #self.title=''    #self.author=''    #self.creationtime=''    #self.filename=''    #self.filetype=''    #self.pages=''
    
 
class public:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('public')
        else:
            self.node = node
            
        #self.publicId = ''
        #slf.uri = ''

   
class lp:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('lp')
        else:
            self.node = node
            
    def set_name(self,name):
        self.node.set('name',name)
        
    def set_version(self,version):
        self.node.set('version',version)
        
    def set_timestamp(self,timestamp=None):
        if timestamp is None:
            import time
            timestamp = time.strftime('%Y-%m-%dT%H:%M:%S%Z')
        self.node.set('timestamp',timestamp)
        
    def get_node(self):
        return self.node
        
    
class linguisticProcessors:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('linguisticProcessors')
        else:
            self.node = node
            
    def get_layer(self):
        return self.node.get('layer')
    
    def set_layer(self,layer):
        self.node.set('layer',layer)
    
    def add_linguistic_processor(self,my_lp):
        self.node.append(my_lp.get_node())
        
    def get_node(self):
        return self.node

    
class nafHeader:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('nafHeader')
        else:
            self.node = node
      
    def add_linguistic_processors(self,linpro):
        self.node.append(linpro.get_node())
        
    def add_linguistic_processor(self, layer ,my_lp):
        ## Locate the linguisticProcessor element for taht layer
        found_lp_obj = None
        for this_lp in self.node.findall('linguisticProcessors'):
            lp_obj = linguisticProcessors(this_lp)
            if lp_obj.get_layer() == layer:
                found_lp_obj = lp_obj
                break
        
        if found_lp_obj is None:    #Not found
            found_lp_obj = linguisticProcessors()
            found_lp_obj.set_layer(layer)
            self.node.add_linguistic_processors(found_lp_obj)
            
        found_lp_obj.add_linguistic_processor(my_lp)
        
        
            
    
         
  
  
## To try if it works
if __name__ == '__main__':
    from lxml import etree
    data = '''  <nafHeader>
                <fileDesc title="3_3012" author="casa400"
                filename="residence_hostal"
                filetype="PDF" pages="19"/>
                <public publicId="3_3012"
                uri="http://casa400.com/docs/residence.pdf" />
                <linguisticProcessors layer="text">
                <lp name="Freeling" version="2.1"
                timestamp="2012-06-25T10:05:00Z"/>
                </linguisticProcessors>
                <linguisticProcessors layer="terms">
                <lp name="Freeling" version="2.1"
                timestamp="2009-06-25T10:10:19Z"/>
                <lp name="ukb" version="0.1.2" timestamp="2012-06-25T16:10:19Z"/>
                </linguisticProcessors>
                <linguisticProcessors layer="namedEntities">
                <lp name="kybot_NE" version="0.1"
                timestamp="2012-06-26T00:10:19Z"/>
                </linguisticProcessors>
                </nafHeader>'''
    node = etree.fromstring(data, parser=None, base_url=None)
    obj = nafHeader(node)
    print obj
    
    