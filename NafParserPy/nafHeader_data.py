class fileDesc:
  def __init__(self,node):
    self.title=''
    self.author=''
    self.creationtime=''
    self.filename=''
    self.filetype=''
    self.pages=''
    
    if node is not None:
      self.title = node.get('title','')
      self.author = node.get('author','')
      self.creationtime=node.get('creationtime','')
      self.filename = node.get('filename','')
      self.filetype = node.get('filetype','')
      self.pages= node.get('pages')
      
  def __str__(self):
      s = 'FileDesc:\n'
      s += '  Title: '+self.title+'\n'
      s += '  Author: '+self.author+'\n'
      s += '  Creationtime: '+self.creationtime+'\n'
      s += '  Filename: '+self.filename+'\n'
      s += '  Filetype: '+self.filetype+'\n'
      s += '  Pages: '+self.pages+'\n'
      s += '\n'
      return s
  
class public:
    def __init__(self,node):
        self.publicId = ''
        self.uri = ''
        if node is not None:
            self.publicId = node.get('publicId','')
            self.uri = node.get('uri','')
    def __str__(self):
        s = 'Public\n'
        s += '  publicId: '+self.publicId+'\n'
        s += '  uri :'+self.uri+'\n'
        return s
   
class lp:
    def __init__(self,node):
        self.name = ''
        self.version =''
        self.timestamp = ''
        if node is not None:
            self.name = node.get('name','')
            self.version = node.get('version','')
            self.timestamp = node.get('timestamp','')
            
    def __str__(self):
        s = 'Lp:'+'\n'
        s += '  Name: '+self.name+'\n'
        s += '  Version: '+self.version+'\n'
        s += '  Timestamp: '+self.timestamp+'\n'
        s += '\n'
        return s
    
class linguisticProcessors:
    def __init__(self,node):
        self.layer = ''
        self.lps =  []
        if node is not None:
            self.layer = node.get('layer','')
            for lp_node in node.findall('lp'):
                self.lps.append(lp(lp_node))
        
    def __str__(self):
        s = 'linguisticProcessors\n'
        s += '  layer:'+ self.layer+'\n'
        for mylp in self.lps:
            s += '  '+str(mylp)+'\n'
        s +='\n'
        return s
    
class nafHeader:
  def __init__(self,node):
    self.fileDesc = None
    self.public = None
    self.linguisticProcessors = []
    
    node_filedesc = node.find('fileDesc')
    if node_filedesc is not None:
        self.fileDesc = fileDesc(node_filedesc)
    
    node_public = node.find('public')
    if node_public is not None:
        self.public = public(node_public)
        
    for lp_node in node.findall('linguisticProcessors'):
        self.linguisticProcessors.append(linguisticProcessors(lp_node))
        
    
  def __str__(self):
      s = 'nafHeader\n'
      s += str(self.fileDesc)
      s += str(self.public)
      for lp in self.linguisticProcessors:
          s += str(lp)+'\n'
      return s 
  
  
  
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
    
    