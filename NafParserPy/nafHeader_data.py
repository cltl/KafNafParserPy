from lxml import etree

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
        
        #self.name = ''        self.version =''        self.timestamp = ''
    
class linguisticProcessors:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('linguisticProcessors')
        else:
            self.node = node
            
        #self.layer = ''
        #self.lps =  []

    
class nafHeader:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('nafHeader')
        else:
            self.node = node
      
    #self.fileDesc = None
    #self.public = None
    #self.linguisticProcessors = []
    
         
  
  
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
    
    