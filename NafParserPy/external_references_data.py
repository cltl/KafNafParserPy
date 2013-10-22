from term_sentiment_data import term_sentiment
from lxml import etree

class externalReference:
    def __init__(self,node=None):
        #self.resource = self.reference = self.reftype = self.status = self.source = self.confidence = ''
        if node is None:
            self.node = etree.Element('externalRef')
        else:
            self.node = node
        
    def get_node(self):
        return self.node
        
    def set_resource(self,resource):
        self.node.set('resource',resource)
    
    def set_confidence(self,confidence):
        self.node.set('confidence',confidence)
    
    def set_reference(self,reference):
        self.node.set('reference',reference)
        

class externalReferences:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('externalReferences')
        else:
            self.node = node
                
    def add_external_reference(self,ext_ref):
        self.node.append(ext_ref.get_node())
        
    def get_node(self):
        return self.node
        

if __name__=='__main__':
    from lxml import etree
    data2 = '''
    <externalReferences>
    <externalRef resource="WN-1.7" reference="eng-17-00861095-v" confidence="0.80">
        <externalRef resource="ontology" reference="Teach" reftype="SubClassOf">
             <externalRef resource="WN-1.7" reftype='sdsd' reference="eng-17-00859568-v" confidence="0.20">
                 <externalRef resource="WN-1.7" reftype='sdsd' reference="eng-17-00859568-v" confidence="0.69"/>
             </externalRef>
        </externalRef>
    </externalRef>
</externalReferences>
'''
    data='''
<externalReferences>
<externalRef resource="WN-ENG" reference="c_1009" conf="0.38">
<sentiment resource="VUA_polarityLexicon_synset" polarity="positive"
strength="average" subjectivity="subjective"
sentiment_semantic_type="behaviour/traitEvaluation"/>
</externalRef>
<externalRef resource="WN-ENG" reference="c_1008" conf="0.31">

</externalRef>
</externalReferences>
'''
    obj = etree.fromstring(data2, parser=None, base_url=None)
    node = externalReferences(obj)
    print node    
    